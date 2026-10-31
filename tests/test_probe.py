"""
Unit tests for sonda_huawei package.
"""

import unittest
from sonda_huawei import __version__
from sonda_huawei.probe import parse_ping_output
from sonda_huawei.cli import build_parser, format_table


class TestHuaweiProbeParsing(unittest.TestCase):

    def test_parse_ping_success_float(self):
        output = """
  PING 8.8.8.8: 56  data bytes, press CTRL_C to break
    Reply from 8.8.8.8: bytes=56 Sequence=1 ttl=118 time=12 ms
    Reply from 8.8.8.8: bytes=56 Sequence=2 ttl=118 time=11 ms
    Reply from 8.8.8.8: bytes=56 Sequence=3 ttl=118 time=14 ms

  --- 8.8.8.8 ping statistics ---
    5 packet(s) transmitted
    5 packet(s) received
    0.00% packet loss
    round-trip min/avg/max = 11.2/12.4/14.1 ms
"""
        res = parse_ping_output(output, source_ip="200.1.1.1", target="8.8.8.8")
        self.assertEqual(res["source_ip"], "200.1.1.1")
        self.assertEqual(res["target"], "8.8.8.8")
        self.assertEqual(res["packet_loss_pct"], 0.0)
        self.assertEqual(res["rtt_min_ms"], 11.2)
        self.assertEqual(res["rtt_avg_ms"], 12.4)
        self.assertEqual(res["rtt_max_ms"], 14.1)

    def test_parse_ping_partial_loss_alt_format(self):
        output = """
  --- 8.8.8.8 ping statistics ---
    5 packet(s) transmitted
    4 packet(s) received
    20.00% packet loss
    min/avg/max = 10/15/20 ms
"""
        res = parse_ping_output(output, source_ip="200.2.2.2", target="8.8.8.8")
        self.assertEqual(res["packet_loss_pct"], 20.0)
        self.assertEqual(res["rtt_min_ms"], 10.0)
        self.assertEqual(res["rtt_avg_ms"], 15.0)
        self.assertEqual(res["rtt_max_ms"], 20.0)

    def test_parse_ping_total_loss(self):
        output = """
  --- 8.8.8.8 ping statistics ---
    5 packet(s) transmitted
    0 packet(s) received
    100.00% packet loss
"""
        res = parse_ping_output(output, source_ip="200.3.3.3", target="8.8.8.8")
        self.assertEqual(res["packet_loss_pct"], 100.0)
        self.assertIsNone(res["rtt_min_ms"])
        self.assertIsNone(res["rtt_avg_ms"])
        self.assertIsNone(res["rtt_max_ms"])


class TestHuaweiCLI(unittest.TestCase):

    def test_version(self):
        self.assertEqual(__version__, "0.1.0")

    def test_parser_valid_args(self):
        parser = build_parser()
        args = parser.parse_args([
            "--host", "192.168.1.1",
            "-u", "admin",
            "-p", "secret",
            "-P", "2222",
            "-t", "8.8.8.8",
            "-s", "200.1.1.1", "200.2.2.2",
            "-c", "10",
            "--size", "128",
            "--json"
        ])
        self.assertEqual(args.host, "192.168.1.1")
        self.assertEqual(args.username, "admin")
        self.assertEqual(args.password, "secret")
        self.assertEqual(args.port, 2222)
        self.assertEqual(args.target, "8.8.8.8")
        self.assertEqual(args.sources, ["200.1.1.1", "200.2.2.2"])
        self.assertEqual(args.count, 10)
        self.assertEqual(args.size, 128)
        self.assertTrue(args.json)

    def test_format_table(self):
        results = [
            {
                "source_ip": "200.1.1.1",
                "target": "8.8.8.8",
                "packet_loss_pct": 0.0,
                "rtt_min_ms": 10.0,
                "rtt_avg_ms": 12.5,
                "rtt_max_ms": 15.0,
            }
        ]
        table = format_table(results)
        self.assertIn("200.1.1.1", table)
        self.assertIn("8.8.8.8", table)
        self.assertIn("0.0%", table)
        self.assertIn("12.5 ms", table)


if __name__ == "__main__":
    unittest.main()

