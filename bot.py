import os
import discord
from discord.ext import commands
from discord import app_commands

# ============================================================
# 풍뢰부대 Discord 구축 봇
# Python 3.10+ / discord.py 2.x
#
# 환경변수:
#   DISCORD_TOKEN = 봇 토큰
#
# 주의:
# - 새 서버에서 먼저 테스트하세요.
# - 봇 초대 시 Manage Roles, Manage Channels, Manage Server,
#   View Channels, Send Messages, Read Message History 권한이 필요합니다.
# - Developer Portal에서 Server Members Intent와 Message Content Intent를 켜세요.
# ============================================================

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------------------------------------------------
# 역할 및 색상
# 역할은 낮은 계급부터 높은 계급 순으로 생성됩니다.
# ------------------------------------------------------------

ROLE_CONFIG = {
    # 이용자 및 인증
    "미인증": "#9E9E9E",
    "인증": "#4CAF50",

    # 병
    "이병": "#90A4AE",
    "일병": "#78909C",
    "상병": "#607D8B",
    "병장": "#455A64",

    # 부사관
    "하사": "#9E9D24",
    "중사": "#C0CA33",
    "상사": "#FDD835",
    "원사": "#FBC02D",
    "주임원사": "#F9A825",

    # 위관급 장교
    "소위": "#80CBC4",
    "중위": "#26A69A",
    "대위": "#00897B",

    # 영관급 장교
    "소령": "#5C6BC0",
    "중령": "#3F51B5",
    "대령": "#3949AB",

    # 장성급 장교
    "준장": "#E57373",
    "소장": "#D84343",
    "중장": "#C62828",
    "대장": "#B71C1C",

    # 장관급 / 최고 지휘부
    "의무사령관": "#D81B60",
    "특수전사령관": "#2E7D32",
    "군사경찰청장": "#00838F",
    "육군참모총장": "#1565C0",
    "국방부장관": "#6A1B9A",
    "참모총장": "#8E24AA",
    "부사령관": "#E53935",
    "총사령관": "#C62828",
    "부그룹홀더": "#FF6B35",
    "그룹홀더": "#FF1F36",

    # 운영 및 인증
    "운영진": "#FF9800",
    "인증처리관": "#00ACC1",

    # TDC
    "TDC": "#7E57C2",
    "TDC 사령관": "#512DA8",
    "TDC 부사령관": "#673AB7",
    "TDC 단장": "#9575CD",

    # MP
    "MP": "#00838F",
    "MP 사령관": "#006064",
    "MP 부사령관": "#00838F",
    "MP 단장": "#4DB6AC",

    # SWC
    "SWC": "#2E7D32",
    "SWC 사령관": "#1B5E20",
    "SWC 부사령관": "#2E7D32",
    "SWC 단장": "#66BB6A",

    # 의무부대
    "의무부사령관": "#C2185B",
    "의무단장": "#F06292",

    # 교육부대
    "교육사령관": "#F9A825",
    "교육부사령관": "#FBC02D",
    "교육단장": "#FFEE58",

    # 행정부
    "행정처장": "#546E7A",
    "행정부처장": "#607D8B",
    "행정단장": "#90A4AE",
}

# 역할의 생성/표시 순서 (아래쪽 역할부터 생성)
ROLE_ORDER = list(ROLE_CONFIG.keys())

# 입·퇴장 채널을 볼 수 있는 역할
STAFF_ACCESS_ROLES = {
    "그룹홀더",
    "부그룹홀더",
    "총사령관",
    "부사령관",
    "참모총장",
    "국방부장관",
    "운영진",
}

# 인증 카테고리에 접근 가능한 역할
VERIFY_ACCESS_ROLES = {"미인증", "인증처리관"}

# 로그 채널 이름
LOG_CHANNEL_NAMES = {
    "『🎒』ㅣ서버 로그",
    "『🎒』ㅣ채팅 로그",
    "『🎒』ㅣ추방 로그",
    "『🎒』ㅣ처벌 로그",
}

# ------------------------------------------------------------
# 서버 구성
# ------------------------------------------------------------

SERVER_STRUCTURE = [
    {
        "category": "▬▬▬《👋ㅣ입ㆍ퇴장》▬▬▬",
        "access": "staff",
        "channels": [
            ("text", "『👋』ㅣ입장"),
            ("text", "『👋』ㅣ퇴장"),
        ],
    },
    {
        "category": "▬▬▬《✅️ㅣ인증》▬▬▬",
        "access": "verify",
        "channels": [
            ("text", "『✅️』ㅣ인증"),
            ("text", "『✅️』ㅣ인증 양식"),
        ],
    },
    {
        "category": "▬▬▬《📢ㅣ공지사항》▬▬▬",
        "access": "verified",
        "channels": [
            ("text", "『📢』ㅣ공지사항"),
            ("text", "『📻』ㅣ커뮤니티 공지"),
            ("text", "『🗳』ㅣ투표"),
            ("text", "『🎉』ㅣ이벤트"),
            ("text", "『🚫』ㅣ블랙리스트"),
            ("text", "『🎖』ㅣ훈장"),
            ("text", "『🎖』ㅣ명예의전당"),
        ],
    },
    {
        "category": "▬▬▬《🌐ㅣ커뮤니티》▬▬▬",
        "access": "verified",
        "channels": [
            ("text", "『💬』ㅣ자유채팅"),
            ("text", "『🧾』ㅣ자유 포럼"),
            ("text", "『🤖』ㅣ봇 명령어"),
            ("forum", "『🚨』ㅣ분쟁해결"),
            ("text", "『🚨』ㅣ신고"),
        ],
    },
    {
        "category": "▬▬▬《📣ㅣ모집》▬▬▬",
        "access": "verified",
        "channels": [
            ("text", "『📋』ㅣ스카웃"),
            ("text", "『📣』ㅣ모집공고"),
        ],
    },
    {
        "category": "▬▬▬《📋ㅣ보고서》▬▬▬",
        "access": "verified",
        "channels": [
            ("text", "『📋』ㅣTDC 보고서"),
            ("text", "『📋』ㅣMP 보고서"),
            ("text", "『📋』ㅣSWC 보고서"),
            ("text", "『📋』ㅣ중요인사 보고서"),
            ("text", "『📋』ㅣ타임아웃 보고서"),
            ("text", "『📋』ㅣ처벌 보고서"),
        ],
    },
    {
        "category": "▬▬▬《📚ㅣ정보》▬▬▬",
        "access": "verified",
        "channels": [
            ("text", "『📖』ㅣ법"),
            ("text", "『📙』ㅣ역사"),
            ("text", "『📕』ㅣ조직도"),
            ("text", "『📘』ㅣ계급"),
        ],
    },
    {
        "category": "▬▬▬《🎒ㅣ로그》▬▬▬",
        "access": "logs",
        "channels": [
            ("text", "『🎒』ㅣ서버 로그"),
            ("text", "『🎒』ㅣ채팅 로그"),
            ("text", "『🎒』ㅣ추방 로그"),
            ("text", "『🎒』ㅣ처벌 로그"),
        ],
    },
]

def get_role(guild: discord.Guild, name: str):
    return discord.utils.get(guild.roles, name=name)


def role_color(hex_color: str) -> discord.Color:
    return discord.Color(int(hex_color.lstrip("#"), 16))


async def create_or_update_role(guild: discord.Guild, name: str):
    """역할이 없으면 만들고, 있으면 색상을 갱신합니다."""
    role = get_role(guild, name)
    color = role_color(ROLE_CONFIG[name])

    if role is None:
        permissions = discord.Permissions.none()
        # 최고 관리자만 Administrator 권한을 가집니다.
        if name == "그룹홀더":
            permissions.administrator = True

        role = await guild.create_role(
            name=name,
            color=color,
            permissions=permissions,
            mentionable=False,
            reason="풍뢰부대 역할 자동 구성",
        )
    else:
        # 기존 역할의 권한은 덮어쓰지 않고 색상만 갱신합니다.
        if role.color != color:
            await role.edit(color=color, reason="풍뢰부대 역할 색상 갱신")

    return role


def build_overwrites(guild: discord.Guild, access: str):
    """카테고리별 기본 열람 권한을 만듭니다."""
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(
            view_channel=False
        )
    }

    if access == "staff":
        allowed_names = STAFF_ACCESS_ROLES
    elif access == "verify":
        allowed_names = VERIFY_ACCESS_ROLES
    elif access == "verified":
        allowed_names = {"인증"}
    else:  # logs
        allowed_names = set()

    for name in allowed_names:
        role = get_role(guild, name)
        if role:
            overwrites[role] = discord.PermissionOverwrite(
                view_channel=True,
                read_message_history=True,
                send_messages=True,
            )

    # 로그는 인증자에게 공개하지 않고, 고위직 및 인증처리관만 열람합니다.
    if access == "logs":
        for name in STAFF_ACCESS_ROLES | {"인증처리관"}:
            role = get_role(guild, name)
            if role:
                overwrites[role] = discord.PermissionOverwrite(
                    view_channel=True,
                    read_message_history=True,
                    send_messages=True,
                )

    return overwrites


async def get_or_create_category(guild: discord.Guild, name: str, access: str):
    category = discord.utils.get(guild.categories, name=name)
    overwrites = build_overwrites(guild, access)

    if category is None:
        category = await guild.create_category(
            name=name,
            overwrites=overwrites,
            reason="풍뢰부대 카테고리 생성",
        )
    else:
        # 기존 카테고리도 권한을 새 설정에 맞춥니다.
        await category.edit(
            overwrites=overwrites,
            reason="풍뢰부대 카테고리 권한 갱신",
        )

    return category


async def create_channel_if_missing(
    guild: discord.Guild,
    category: discord.CategoryChannel,
    channel_type: str,
    name: str,
):
    existing = discord.utils.get(guild.channels, name=name)

    if existing is not None:
        # 같은 이름의 채널이 다른 카테고리에 있어도 중복 생성하지 않습니다.
        # 기존 채널 권한은 건드리지 않습니다.
        return existing

    if channel_type == "forum":
        return await guild.create_forum(
            name=name,
            category=category,
            topic="풍뢰부대 분쟁 해결 및 중재 포럼",
            reason="풍뢰부대 분쟁해결 포럼 생성",
        )

    return await guild.create_text_channel(
        name=name,
        category=category,
        reason="풍뢰부대 채널 생성",
    )


async def build_server(guild: discord.Guild):
    # 서버 이름 변경
    if guild.name != "풍뢰부대":
        await guild.edit(name="풍뢰부대", reason="풍뢰부대 서버 자동 구성")

    # 역할 생성 및 색상 적용
    for role_name in ROLE_ORDER:
        await create_or_update_role(guild, role_name)

    # 카테고리와 채널 생성
    for item in SERVER_STRUCTURE:
        category = await get_or_create_category(
            guild, item["category"], item["access"]
        )
        for channel_type, channel_name in item["channels"]:
            await create_channel_if_missing(
                guild, category, channel_type, channel_name
            )

    # 안내: 자동 인증 패널은 아직 포함하지 않습니다.
    return True


async def send_log(guild: discord.Guild, channel_name: str, message: str):
    channel = discord.utils.get(guild.text_channels, name=channel_name)
    if channel is None:
        return
    try:
        await channel.send(message)
    except discord.Forbidden:
        print(f"로그 전송 권한 없음: {channel_name}")


# ------------------------------------------------------------
# 이벤트 로그
# ------------------------------------------------------------

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"슬래시 명령어 동기화 완료: {len(synced)}개")
    except Exception as error:
        print(f"슬래시 명령어 동기화 실패: {error}")

    print(f"로그인 성공: {bot.user} (ID: {bot.user.id})")


@bot.event
async def on_member_join(member: discord.Member):
    # 신규 가입자는 미인증 역할을 받습니다.
    role = get_role(member.guild, "미인증")
    if role:
        try:
            await member.add_roles(role, reason="신규 가입자 미인증 역할")
        except discord.Forbidden:
            print("미인증 역할 지급 실패: 봇 역할 위치와 권한을 확인하세요.")

    await send_log(
        member.guild,
        "『👋』ㅣ입장",
        f"👋 {member.mention} 님이 풍뢰부대에 입장했습니다.",
    )
    await send_log(
        member.guild,
        "『🎒』ㅣ서버 로그",
        f"➕ 가입: {member} (`{member.id}`)",
    )


@bot.event
async def on_member_remove(member: discord.Member):
    await send_log(
        member.guild,
        "『👋』ㅣ퇴장",
        f"👋 **{member}** 님이 풍뢰부대에서 퇴장했습니다.",
    )
    await send_log(
        member.guild,
        "『🎒』ㅣ서버 로그",
        f"➖ 퇴장: {member} (`{member.id}`)",
    )


@bot.event
async def on_member_ban(guild: discord.Guild, user: discord.User):
    await send_log(
        guild,
        "『🎒』ㅣ추방 로그",
        f"🔨 차단: {user} (`{user.id}`)",
    )


# ------------------------------------------------------------
# ^^^ 입력 시 서버 구성 설명
# 실제 입력은 ^^^ 이며, prefix는 ! 이므로 명령어는 !^^^ 입니다.
# 아래에서 별도 메시지 감지로 ^^^ 자체를 지원합니다.
# ------------------------------------------------------------

# ------------------------------------------------------------
# 슬래시 명령어
# ------------------------------------------------------------

@bot.tree.command(
    name="풍뢰부대",
    description="풍뢰부대 서버 역할, 카테고리, 채널을 생성하고 권한을 설정합니다.",
)
@app_commands.checks.has_permissions(manage_guild=True)
async def build_fungroe(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message(
            "이 명령어는 서버 안에서만 사용할 수 있습니다.",
            ephemeral=True,
        )
        return

    await interaction.response.defer(ephemeral=True, thinking=True)

    try:
        await build_server(interaction.guild)
        await interaction.followup.send(
            "⚡ **풍뢰부대 서버 구성이 완료되었습니다.**\n"
            "역할 색상, 카테고리, 채널 및 기본 권한을 확인해 주세요.\n\n"
            "참고: 인증 버튼/양식 처리, 신고 처리, 처벌 자동 기록은 별도 기능입니다.",
            ephemeral=True,
        )
    except discord.Forbidden:
        await interaction.followup.send(
            "❌ 봇 권한이 부족합니다. 채널 관리, 역할 관리, 서버 관리 권한을 "
            "확인하고 봇 역할을 관리할 역할보다 위로 올려 주세요.",
            ephemeral=True,
        )
    except Exception as error:
        print(f"서버 구성 오류: {repr(error)}")
        await interaction.followup.send(
            f"❌ 실행 중 오류가 발생했습니다: `{type(error).__name__}: {error}`",
            ephemeral=True,
        )


@build_fungroe.error
async def build_fungroe_error(
    interaction: discord.Interaction, error: app_commands.AppCommandError
):
    if isinstance(error, app_commands.MissingPermissions):
        message = "이 명령어는 서버 관리 권한이 있는 사람만 사용할 수 있습니다."
    else:
        message = f"명령어 오류: {error}"

    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)


# ------------------------------------------------------------
# 일반 메시지 명령어: ^^^
# ------------------------------------------------------------

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.guild:
        # ^^^는 메시지 내용 인텐트가 필요합니다.
        if message.content.strip() == "^^^":
            embed = discord.Embed(
                title="⚡ 풍뢰부대 서버 구성 안내",
                description=(
                    "**서버 이름:** 풍뢰부대\n\n"
                    "👋 **입·퇴장:** 지정된 고위직 전용\n"
                    "✅ **인증:** 미인증 및 인증처리관 전용\n"
                    "📢 **공지사항:** 인증 완료자 전용\n"
                    "🌐 **커뮤니티:** 인증 완료자 전용\n"
                    "📣 **모집:** 인증 완료자 전용\n"
                    "📋 **보고서:** 인증 완료자 전용\n"
                    "📚 **정보:** 인증 완료자 전용\n"
                    "🎒 **로그:** 고위직 및 인증처리관 전용\n\n"
                    "🚨 분쟁해결은 포럼 채널입니다.\n"
                    "🎖 역할에는 계급, 직책, 색상이 포함됩니다."
                ),
                color=discord.Color.from_str("#1565C0"),
            )
            await message.channel.send(embed=embed)

        # 채팅 로그
        log_message = (
            f"**#{message.channel.name}** | {message.author} "
            f"(`{message.author.id}`): {message.content[:1500]}"
        )
        await send_log(message.guild, "『🎒』ㅣ채팅 로그", log_message)

    await bot.process_commands(message)


# ------------------------------------------------------------
# 실행
# ------------------------------------------------------------

if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN 환경변수가 없습니다. 호스팅 사이트의 Environment Variables에 "
        "DISCORD_TOKEN 이름으로 봇 토큰을 설정하세요."
    )

bot.run(TOKEN)
