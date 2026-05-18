import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
COLORS_CHANNEL_ID = 1505747026644832377

COLORS_TO_CREATE = [
    ("Red",                 0xFF4444, "Level 5"),
    ("Blue",                0x4488FF, "Level 5"),
    ("Green",               0x44CC44, "Level 5"),
    ("Yellow",              0xFFDD44, "Level 5"),
    ("Orange",              0xFF8844, "Level 5"),
    ("Teal",                0x44CCCC, "Level 15"),
    ("Purple",              0xAA44FF, "Level 15"),
    ("Pink",                0xFF88CC, "Level 15"),
    ("Lime",                0x88FF44, "Level 15"),
    ("Sky",                 0x44BBFF, "Level 15"),
    ("Crimson",             0xCC0033, "Level 30"),
    ("Navy",                0x003399, "Level 30"),
    ("Emerald",             0x00CC66, "Level 30"),
    ("Magenta",             0xFF00AA, "Level 30"),
    ("Indigo",              0x4444CC, "Level 30"),
    ("District Purple",     0x5B0099, "Level 50"),
    ("Blood Red",           0x8B0000, "Level 75"),
    ("Void",                0x1A0033, "Level 75"),
    ("Toxic",               0x39FF14, "Level 75"),
    ("Storm",               0x00BFFF, "Level 75"),
    ("Galaxy",              0x1B0066, "Level 75"),
    ("Special Silver",       0xC0C0C0, "Level 125"),
    ("VIP Gold",             0xFFD700, "Level 150"),
    ("aStubbyMonkey Purple", 0x9826E9, "Level 200"),
    ("Booster Pink",         0xFF69B4, "Server Booster"),
]

TIERS = [
    {
        "required_id":   1446344992871157851,
        "required_name": "Level 5",
        "label":         "✦ Basic Colors",
        "colors": [
            ("Red",    "🔴"),
            ("Blue",   "🔵"),
            ("Green",  "🟢"),
            ("Yellow", "🟡"),
            ("Orange", "🟠"),
        ],
    },
    {
        "required_id":   1446699112236978267,
        "required_name": "Level 15",
        "label":         "✦ Rare Colors",
        "colors": [
            ("Teal",   "🩵"),
            ("Purple", "🟣"),
            ("Pink",   "🩷"),
            ("Lime",   "💚"),
            ("Sky",    "🔹"),
        ],
    },
    {
        "required_id":   1446345047267213313,
        "required_name": "Level 30",
        "label":         "✦ Epic Colors",
        "colors": [
            ("Crimson", "❤️‍🔥"),
            ("Navy",    "🌊"),
            ("Emerald", "💎"),
            ("Magenta", "🌸"),
            ("Indigo",  "🔮"),
        ],
    },
    {
        "required_id":   1446345091072524368,
        "required_name": "Level 50",
        "label":         "✦ District Color",
        "colors": [
            ("District Purple", "🌑"),
        ],
    },
    {
        "required_id":   1446345093857411132,
        "required_name": "Level 75",
        "label":         "✦ Legendary Colors",
        "colors": [
            ("Blood Red", "🩸"),
            ("Void",      "🫧"),
            ("Toxic",     "☢️"),
            ("Storm",     "⚡"),
            ("Galaxy",    "🌌"),
        ],
    },
    {
        "required_id":   1446345193761669282,
        "required_name": "Level 125",
        "label":         "✦ Special Silver",
        "colors": [
            ("Special Silver", "🩶"),
        ],
    },
    {
        "required_id":   1446345196764925992,
        "required_name": "Level 150",
        "label":         "✦ VIP Gold",
        "colors": [
            ("VIP Gold", "✨"),
        ],
    },
    {
        "required_id":   1446699972379807795,
        "required_name": "Level 200",
        "label":         "✦ aStubbyMonke",
        "colors": [
            ("aStubbyMonkey Purple", "👑"),
        ],
    },
    {
        "required_id":   1505734653322072074,
        "required_name": "Server Booster",
        "label":         "✦ Booster Exclusive",
        "colors": [
            ("Booster Pink", "💗"),
        ],
    },
]

COLOR_ROLE_IDS: dict[str, int] = {
    "Blood Red":           1505743622946029568,
    "Blue":                1505743604218462350,
    "Crimson":             1505743614557421681,
    "District Purple":     1505743621511712778,
    "Emerald":             1505743616633737226,
    "Galaxy":              1505743628100702329,
    "VIP Gold":            1505743630772473859,
    "Green":               1505743605896314960,
    "Indigo":              1505743619938717826,
    "Lime":                1505743612158148791,
    "Magenta":             1505743617854144563,
    "Navy":                1505743615731957831,
    "Orange":              1505743608517497004,
    "Pink":                1505743611533332661,
    "Booster Pink":         1505743633188651058,
    "Purple":              1505743610006601890,
    "Red":                 1505743602838409387,
    "Special Silver":      1505743629778423840,
    "Sky":                 1505743613693526077,
    "Storm":               1505743626096087130,
    "Teal":                1505743609411010682,
    "Toxic":               1505743624934260897,
    "Void":                1505743624091074580,
    "Yellow":              1505743607297081355,
    "aStubbyMonkey Purple": 1505743632177561780,
}

ALL_COLOR_ROLE_IDS: set[int] = set(COLOR_ROLE_IDS.values())

COLOR_REQUIRED: dict[str, tuple[int, str]] = {
    color: (tier["required_id"], tier["required_name"])
    for tier in TIERS
    for color, _ in tier["colors"]
}

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


def member_role_ids(member: discord.Member) -> set[int]:
    return {r.id for r in member.roles}


async def apply_color(interaction: discord.Interaction, color: str):
    member = interaction.user
    guild = interaction.guild
    owned = member_role_ids(member)
    required_id, required_name = COLOR_REQUIRED[color]

    if required_id not in owned:
        await interaction.response.send_message(
            f"🔒 **{color}** is locked — you need **{required_name}** to unlock it.",
            ephemeral=True,
        )
        return

    role_id = COLOR_ROLE_IDS.get(color)
    target_role = guild.get_role(role_id) if role_id else None
    if not target_role:
        await interaction.response.send_message(
            f"❌ Role for **{color}** is missing. Ask an admin to re-run `!create_color_roles`.",
            ephemeral=True,
        )
        return

    old_colors = [r for r in member.roles if r.id in ALL_COLOR_ROLE_IDS]
    if old_colors:
        await member.remove_roles(*old_colors)

    if len(old_colors) == 1 and old_colors[0].id == role_id:
        await interaction.response.send_message(
            f"Removed your **{color}** color.", ephemeral=True
        )
        return

    await member.add_roles(target_role)
    await interaction.response.send_message(
        f"✅ Color set to **{color}**!", ephemeral=True
    )


class ColorDropdown(discord.ui.Select):
    def __init__(self, placeholder: str, custom_id: str, tier_list: list):
        options = []
        for tier in tier_list:
            for color, emoji in tier["colors"]:
                options.append(discord.SelectOption(
                    label=color,
                    emoji=emoji,
                    value=color,
                    description=f"Requires {tier['required_name']}",
                ))
        super().__init__(
            placeholder=placeholder,
            custom_id=custom_id,
            options=options,
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        await apply_color(interaction, self.values[0])


class RemoveColorButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Remove Color",
            emoji="🗑️",
            custom_id="remove_color",
            style=discord.ButtonStyle.danger,
        )

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        old_colors = [r for r in member.roles if r.id in ALL_COLOR_ROLE_IDS]
        if not old_colors:
            await interaction.response.send_message(
                "You don't have a color role to remove.", ephemeral=True
            )
            return
        await member.remove_roles(*old_colors)
        await interaction.response.send_message(
            "🗑️ Removed your color role.", ephemeral=True
        )


class RemoveView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RemoveColorButton())


class ColorRoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(ColorDropdown(
            placeholder="🔴  Basic Colors  —  Level 5",
            custom_id="dropdown_basic",
            tier_list=[t for t in TIERS if t["required_name"] == "Level 5"],
        ))
        self.add_item(ColorDropdown(
            placeholder="🟣  Rare Colors  —  Level 15",
            custom_id="dropdown_rare",
            tier_list=[t for t in TIERS if t["required_name"] == "Level 15"],
        ))
        self.add_item(ColorDropdown(
            placeholder="💎  Epic Colors  —  Level 30",
            custom_id="dropdown_epic",
            tier_list=[t for t in TIERS if t["required_name"] == "Level 30"],
        ))
        self.add_item(ColorDropdown(
            placeholder="🌌  Legendary Colors  —  Level 75",
            custom_id="dropdown_legendary",
            tier_list=[t for t in TIERS if t["required_name"] == "Level 75"],
        ))
        self.add_item(ColorDropdown(
            placeholder="⭐  Exclusive Colors  —  Select to view",
            custom_id="dropdown_exclusives",
            tier_list=[t for t in TIERS if t["required_name"] in (
                "Server Booster", "Level 50", "Level 125", "Level 150", "Level 200"
            )],
        ))


@bot.event
async def on_ready():
    bot.add_view(ColorRoleView())
    bot.add_view(RemoveView())
    print(f"✅ Online as {bot.user}")


@bot.command()
@commands.has_permissions(administrator=True)
async def create_color_roles(ctx):
    await ctx.send("⚙️ Creating color roles...", delete_after=5)
    created = []
    skipped = []

    for name, hex_color, tier_label in COLORS_TO_CREATE:
        existing = discord.utils.get(ctx.guild.roles, name=name)
        if existing:
            COLOR_ROLE_IDS[name] = existing.id
            ALL_COLOR_ROLE_IDS.add(existing.id)
            skipped.append((name, existing.id))
            continue
        role = await ctx.guild.create_role(
            name=name,
            color=discord.Color(hex_color),
            reason=f"Color role for {tier_label}",
        )
        COLOR_ROLE_IDS[name] = role.id
        ALL_COLOR_ROLE_IDS.add(role.id)
        created.append((name, role.id))

    lines = ["```py", "# Paste these into COLOR_ROLE_IDS:"]
    for name, role_id in sorted(created + skipped, key=lambda x: x[0]):
        lines.append(f'"{name}": {role_id},')
    lines.append("```")
    await ctx.send(
        f"✅ Created **{len(created)}** roles, skipped **{len(skipped)}** (already existed).\n" +
        "\n".join(lines)
    )


@bot.command()
@commands.has_permissions(administrator=True)
async def setup_colors(ctx):
    if ctx.channel.id != COLORS_CHANNEL_ID:
        await ctx.message.delete()
        return

    await ctx.message.delete()

    icon = ctx.guild.icon.url if ctx.guild.icon else None

    embed = discord.Embed(color=0x9826E9)
    embed.set_author(name="aStubbyServer  ·  Color Roles", icon_url=icon)
    embed.description = (
        "-# Your name color reflects how far you've come. Level up to unlock rarer colors.\n\n"
        "🔴 **Basic** `Lv 5`　"
        "🟣 **Rare** `Lv 15`　"
        "💎 **Epic** `Lv 30`　"
        "🌌 **Legendary** `Lv 75`\n\n"
        "🌑 **District Purple** `Lv 50`　"
        "🩶 **Special Silver** `Lv 125`　"
        "✨ **VIP Gold** `Lv 150`　"
        "👑 **aStubbyMonkey Purple** `Lv 200`　"
        "💗 **Booster Pink** `Booster`"
    )
    embed.set_footer(text="Use the dropdowns below  ·  Select your current color again to remove it")

    await ctx.send(embed=embed, view=ColorRoleView())
    await ctx.send(view=RemoveView())


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id == COLORS_CHANNEL_ID and not message.author.guild_permissions.administrator:
        await message.delete()
        return
    await bot.process_commands(message)


bot.run(TOKEN)