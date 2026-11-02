 
<div align="center">

# 👋 Welcome

### A customizable Discord welcome bot.

Greet new members with beautiful embeds, dynamic placeholders, and simple slash commands.

<br>

[![Python](https://img.shields.io/badge/Python-3.13+-7c83ff?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-a78bfa?style=for-the-badge)](LICENSE)

<br>

**Make every new member feel welcome.**

</div>

---

## ✦ Features

<table>
<tr>
<td width="50%">

### 🎨 Custom Welcome Embeds
Design your own welcome messages using JSON. Customize titles, descriptions, colors, images, fields, and footers.

</td>
<td width="50%">

### 🧩 Dynamic Placeholders
Personalize messages with member, server, channel, bot, and date information.

</td>
</tr>
<tr>
<td width="50%">

### ⚡ Slash Commands
Manage your welcome system directly from Discord with easy-to-use commands.

</td>
<td width="50%">

### 🗄️ PostgreSQL Storage
Store welcome settings separately for each server using PostgreSQL.

</td>
</tr>
</table>

---

## 🚀 Getting Started

### Requirements

- Python 3.13+
- A Discord application and bot token
- A PostgreSQL database
- Git

### 1. Clone the repository

```bash
git clone https://github.com/surajkyu/discord-welcome.git
cd discord-welcome
```

### 2. Install dependencies

##### Bash shell
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

##### Fish shell
```fish
python -m venv .venv
source .venv/bin/activate.fish
pip install -r requirements.txt
```

##### Powershell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation because of its execution policy

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 3. Configure environment variables

Copy `.env.example` to `.env` in the project root.

##### For Linux/Macos

```bash
cp .env.example .env
```

##### For Windows
```powershell
Copy-Item .env.example .env
```

### 5. Start the bot

```bash
python main.py
```

---

## 💬 Commands

| Command | Description |
|:--|:--|
| `/welcome channel add` | Set the welcome channel |
| `/welcome channel show` | Show the current welcome channel |
| `/welcome channel remove` | Remove the welcome channel |
| `/welcome embed` | Preview and save a custom welcome embed |
| `/welcome test` | Test the welcome message |

---

## 🧩 Custom Embeds

Create your welcome message with JSON:

```json
{
  "content": "Hey, {user.mention}! Welcome to {server.name}!",
  "embeds": [
    {
      "title": "Welcome aboard! ✨",
      "description": "We're glad to have you here.",
      "color": 5793266,
      "footer": {
        "text": "Enjoy your stay!"
      }
    }
  ]
}
```

See the [Wiki](https://github.com/surajkyu/discord-welcome-bot/wiki) for more examples and previews.

Upload your JSON file using `/welcome embed` to preview it. Save the embed when you're happy with the result.

---

## 🏷️ Placeholders

Use placeholders to add dynamic information to your messages.

| Placeholder | Description |
|:--|:--|
| `{user}` | Member's name |
| `{user.mention}` | Mention the member |
| `{user.id}` | Member's Discord ID |
| `{user.avatar}` | Member's avatar URL |
| `{server.name}` | Server name |
| `{server.member_count}` | Server member count |
| `{server.owner}` | Server owner |
| `{channel.mention}` | Welcome channel mention |
| `{date}` | Current date |
| `{time}` | Current time |
| `{bot.name}` | Bot name |

See the [Wiki](https://github.com/surajkyu/discord-welcome-bot/wiki) for the full placeholder list.

---

## 📖 Documentation

| Resource | Description |
|:--|:--|
| [Wiki](https://github.com/surajkyu/discord-welcome-bot/wiki) | Setup guides, examples, and placeholders |
| [Discord.py](https://discordpy.readthedocs.io/) | Discord library documentation |
| [Discord Developer Portal](https://discord.com/developers/applications) | Create and manage your bot |

---

## 🤝 Contributing

Contributions, ideas, and bug reports are welcome.

1. Fork the repository.
2. Create a branch for your changes.
3. Commit your changes.
4. Open a pull request.

---

## 📄 License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.

<div align="center">

<br>

**Made with Python 💜**

</div>

