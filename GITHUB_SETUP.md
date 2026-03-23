# Configuração de Credenciais para GitHub

## Estado Atual

Sua configuração Git está pronta para sincronizar com o GitHub:

| Configuração | Valor |
|--------------|-------|
| **Remote** | `https://github.com/LucasCinigalia/ai-integrator.git` |
| **Branch** | `main` |
| **Nome** | Lucas Cinigalia |
| **Email** | cinigalialucas@gmail.com |
| **Credential Helper** | Git Credential Manager |

## Como Autenticar no GitHub

O GitHub não aceita mais senhas. Use um dos métodos abaixo:

### Opção 1: Token de Acesso Pessoal (PAT) – recomendado para HTTPS

1. Acesse: **GitHub → Settings → Developer settings → Personal access tokens**
   - Link direto: https://github.com/settings/tokens

2. Clique em **"Generate new token (classic)"**

3. Configure:
   - **Note**: `ai-integrator` (ou outro nome)
   - **Expiration**: 90 days ou No expiration
   - **Scopes**: marque `repo` (acesso completo aos repositórios)

4. Clique em **Generate token** e copie o token (começa com `ghp_`).

5. Quando o Git pedir credenciais:
   - **Username**: seu nome de usuário do GitHub (`LucasCinigalia`)
   - **Password**: cole o token (não a senha da conta)

6. O Git Credential Manager guarda o token no Windows.

### Opção 2: GitHub CLI

```powershell
# Instalar GitHub CLI (se não tiver)
winget install GitHub.cli

# Fazer login
gh auth login
```

Depois disso, o `git push` passa a usar automaticamente o GitHub CLI.

### Opção 3: SSH (sem token no dia a dia)

```powershell
# Gerar chave SSH
ssh-keygen -t ed25519 -C "cinigalialucas@gmail.com" -f $env:USERPROFILE\.ssh\id_ed25519_github

# Adicionar chave ao agent
ssh-add $env:USERPROFILE\.ssh\id_ed25519_github

# Copiar chave pública (adicione em GitHub → Settings → SSH keys)
Get-Content $env:USERPROFILE\.ssh\id_ed25519_github.pub

# Trocar remote para SSH
git remote set-url origin git@github.com:LucasCinigalia/ai-integrator.git
```

## Comandos para Sincronizar

```powershell
# Enviar commits para o GitHub
git push origin main

# Baixar alterações do GitHub
git pull origin main

# Verificar status
git status
```

## Solução de Problemas

**Erro "Authentication failed":**
- Confirme se está usando o **token** e não a senha.
- Verifique se o token tem o escopo `repo`.

**Esquecer credenciais salvas:**
```powershell
# Abrir Gerenciador de Credenciais do Windows
cmdkey /list | findstr git
# Remover credenciais antigas: Painel de Controle → Credenciais do Windows
```
