# Ciclo de Lançamentos e Manutenção de Releases

[**Português**](RELEASING.md) | [English](RELEASING.en.md)

Este documento detalha o procedimento para lançar novas versões do **Sonda-Huawei** e sincronizar os ecossistemas de distribuição (**FreeBSD Ports** e **Homebrew Tap**).

---

## 🏷️ Versionamento

O projeto adota o [Versionamento Semântico](https://semver.org/lang/pt-BR/) (`vMAJOR.MINOR.PATCH`).

- **MAJOR**: Alterações incompatíveis na CLI ou na API interna.
- **MINOR**: Novas funcionalidades (ex: novos comandos VRP, suporte a outros modelos de roteadores).
- **PATCH**: Correções de bugs, regexes de ping, ajustes de dependências e documentação.

---

## 🚀 Passo a Passo para uma Nova Versão

### 1. Atualizar a Versão nos Arquivos do Pacote

Altere a versão para `X.Y.Z`:
1. No arquivo [`pyproject.toml`](../pyproject.toml):
   ```toml
   version = "X.Y.Z"
   ```
2. No arquivo [`sonda_huawei/__init__.py`](../sonda_huawei/__init__.py):
   ```python
   __version__ = "X.Y.Z"
   ```
3. Registre as novidades no [`CHANGELOG.md`](../CHANGELOG.md).

### 2. Validar os Testes Locais

```bash
python3 -m unittest discover -s tests -v
```

### 3. Criar o Commit e a Tag de Release

```bash
git add pyproject.toml sonda_huawei/__init__.py CHANGELOG.md
git commit -m "chore(release): bump version to vX.Y.Z"
git tag -a vX.Y.Z -m "Release vX.Y.Z"

git push origin main
git push origin vX.Y.Z
```

O workflow de CI/CD [`.github/workflows/release.yml`](../.github/workflows/release.yml) será disparado automaticamente:
- Validação cruzada da tag com `pyproject.toml`.
- Build dos pacotes sdist (`.tar.gz`) e wheel (`.whl`).
- Geração dos checksums `SHA256SUMS`.
- Publicação da Release oficial no GitHub com os artefatos anexados.

---

## 📦 Atualização dos Canais de Distribuição

Após a publicação da tag no GitHub, utilize o script auxiliar para extrair os hashes exatos:

```bash
./ci/update-release-hashes.sh X.Y.Z
```

### 🔹 FreeBSD Port (`freebsd/`)

1. Atualize a versão no [`freebsd/Makefile`](../freebsd/Makefile):
   ```makefile
   DISTVERSION=    X.Y.Z
   ```
2. Substitua os dados no [`freebsd/distinfo`](../freebsd/distinfo) com o output gerado pelo script.
3. Commit e push no repositório:
   ```bash
   git add freebsd/Makefile freebsd/distinfo
   git commit -m "feat(freebsd): update port to vX.Y.Z"
   git push origin main
   ```

### 🔹 Homebrew Tap (`Formula/sonda-huawei.rb`)

No repositório do tap ([cleberalves40/homebrew-tap](https://github.com/cleberalves40/homebrew-tap)):
1. Atualize a URL e o `sha256` em `Formula/sonda-huawei.rb`:
   ```ruby
   url "https://github.com/cleberalves40/Sonda-Huawei/archive/refs/tags/vX.Y.Z.tar.gz"
   sha256 "<novo-sha256>"
   ```
2. Commit e push na branch `main`:
   ```bash
   git commit -am "sonda-huawei X.Y.Z"
   git push origin main
   ```
O workflow do tap testará e auditará a instalação da nova versão.

