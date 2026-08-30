import os
import shutil
import subprocess
import textwrap
import time
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


# ============================================================
# TIMEFLOW WALLPAPER SYNC
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

TEXT_FILE = BASE_DIR / "notes.txt"
WALLPAPER_DIR = BASE_DIR / "generated_wallpapers"
WALLPAPER_FILE = WALLPAPER_DIR / "current_wallpaper.png"

CHECK_INTERVAL = 1
PAGE_DURATION = 5


# ============================================================
# SCREEN SIZE
# ============================================================

def get_screen_size():
    """Detect the primary monitor resolution."""

    try:
        output = subprocess.check_output(
            ["xrandr"],
            text=True,
            stderr=subprocess.DEVNULL
        )

        for line in output.splitlines():

            if " connected primary " in line or " connected " in line:

                for part in line.split():

                    if "x" in part and "+" in part:

                        resolution = part.split("+")[0]

                        width, height = resolution.split("x")

                        return int(width), int(height)

    except (FileNotFoundError, subprocess.CalledProcessError, ValueError):
        pass

    # Fallback resolution
    return 1920, 1080


SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_size()


# ============================================================
# FONT
# ============================================================

def find_font(size, bold=False):
    """Find a commonly available Linux font."""

    if bold:

        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
        ]

    else:

        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
        ]

    for font_path in font_paths:

        if os.path.exists(font_path):

            return ImageFont.truetype(
                font_path,
                size
            )

    return ImageFont.load_default()


# ============================================================
# READ TEXT FILE
# ============================================================

def read_text_file():
    """Read the user's text file and return its status."""

    if not TEXT_FILE.exists():

        return None, "missing"

    try:

        content = TEXT_FILE.read_text(
            encoding="utf-8"
        )

    except (OSError, UnicodeError):

        return None, "error"

    if not content.strip():

        return None, "empty"

    return content.strip(), "ok"


# ============================================================
# TEXT WRAPPING
# ============================================================

def wrap_text(draw, text, font, max_width):
    """Wrap text based on the actual rendered width."""

    lines = []

    for paragraph in text.splitlines():

        # Preserve blank lines
        if not paragraph.strip():

            lines.append("")

            continue

        words = paragraph.split()

        current_line = ""

        for word in words:

            test_line = (
                word
                if not current_line
                else current_line + " " + word
            )

            bbox = draw.textbbox(
                (0, 0),
                test_line,
                font=font
            )

            width = bbox[2] - bbox[0]

            if width <= max_width:

                current_line = test_line

            else:

                if current_line:

                    lines.append(current_line)

                # Handle extremely long words
                if draw.textbbox(
                    (0, 0),
                    word,
                    font=font
                )[2] <= max_width:

                    current_line = word

                else:

                    chunks = textwrap.wrap(
                        word,
                        width=max(
                            1,
                            int(max_width / max(font.size * 0.55, 1))
                        ),
                        break_long_words=True,
                        break_on_hyphens=False
                    )

                    if chunks:

                        lines.extend(chunks[:-1])

                        current_line = chunks[-1]

                    else:

                        current_line = ""

        if current_line:

            lines.append(current_line)

    return lines


# ============================================================
# CREATE PAGES
# ============================================================

def create_pages(
    draw,
    content,
    font,
    max_width,
    max_lines
):
    """Split long text into readable wallpaper pages."""

    lines = wrap_text(
        draw,
        content,
        font,
        max_width
    )

    if not lines:

        return [["No content"]]

    pages = []

    for i in range(
        0,
        len(lines),
        max_lines
    ):

        pages.append(
            lines[i:i + max_lines]
        )

    return pages


# ============================================================
# CREATE WALLPAPER
# ============================================================

def create_wallpaper(
    content,
    status,
    page_number=0
):
    """Generate the wallpaper image."""

    image = Image.new(
        "RGB",
        (
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        ),
        (8, 12, 18)
    )

    draw = ImageDraw.Draw(image)


    # --------------------------------------------------------
    # Fonts
    # --------------------------------------------------------

    title_font = find_font(
        34,
        bold=True
    )

    text_font = find_font(
        25
    )

    time_font = find_font(
        72,
        bold=True
    )

    small_font = find_font(
        18
    )


    # --------------------------------------------------------
    # Layout
    # --------------------------------------------------------

    margin_x = max(
        60,
        int(SCREEN_WIDTH * 0.06)
    )

    top = max(
        50,
        int(SCREEN_HEIGHT * 0.07)
    )

    content_width = (
        SCREEN_WIDTH -
        (margin_x * 2)
    )


    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    draw.text(
        (
            margin_x,
            top
        ),
        "TIMEFLOW",
        font=title_font,
        fill=(56, 189, 248)
    )

    draw.text(
        (
            margin_x,
            top + 50
        ),
        "Dynamic Wallpaper Sync",
        font=small_font,
        fill=(120, 140, 160)
    )


    # --------------------------------------------------------
    # Divider
    # --------------------------------------------------------

    divider_y = top + 90

    draw.line(
        (
            margin_x,
            divider_y,
            SCREEN_WIDTH - margin_x,
            divider_y
        ),
        fill=(40, 55, 70),
        width=2
    )


    # --------------------------------------------------------
    # LIVE TIME
    # --------------------------------------------------------

    current_time = datetime.now().strftime(
        "%H:%M:%S"
    )

    current_date = datetime.now().strftime(
        "%A, %d %B %Y"
    )


    time_bbox = draw.textbbox(
        (0, 0),
        current_time,
        font=time_font
    )

    time_width = (
        time_bbox[2] -
        time_bbox[0]
    )


    draw.text(
        (
            SCREEN_WIDTH -
            margin_x -
            time_width,
            top + 25
        ),
        current_time,
        font=time_font,
        fill=(240, 245, 250)
    )


    date_bbox = draw.textbbox(
        (0, 0),
        current_date,
        font=small_font
    )

    date_width = (
        date_bbox[2] -
        date_bbox[0]
    )


    draw.text(
        (
            SCREEN_WIDTH -
            margin_x -
            date_width,
            top + 105
        ),
        current_date,
        font=small_font,
        fill=(120, 140, 160)
    )


    # --------------------------------------------------------
    # CONTENT
    # --------------------------------------------------------

    content_top = divider_y + 65


    # Missing file
    if status == "missing":

        draw.text(
            (
                margin_x,
                content_top
            ),
            "Text file not found",
            font=title_font,
            fill=(248, 113, 113)
        )

        draw.text(
            (
                margin_x,
                content_top + 60
            ),
            f"Create the file: {TEXT_FILE.name}",
            font=text_font,
            fill=(210, 220, 230)
        )


    # Empty file
    elif status == "empty":

        draw.text(
            (
                margin_x,
                content_top
            ),
            "Your file is empty",
            font=title_font,
            fill=(250, 204, 21)
        )

        draw.text(
            (
                margin_x,
                content_top + 60
            ),
            "Add some notes, tasks or plans to notes.txt.",
            font=text_font,
            fill=(210, 220, 230)
        )


    # Reading error
    elif status == "error":

        draw.text(
            (
                margin_x,
                content_top
            ),
            "Unable to read file",
            font=title_font,
            fill=(248, 113, 113)
        )

        draw.text(
            (
                margin_x,
                content_top + 60
            ),
            "Check the file permissions and encoding.",
            font=text_font,
            fill=(210, 220, 230)
        )


    # Normal content
    else:

        pages = create_pages(
            draw,
            content,
            text_font,
            content_width,
            20
        )

        page_number %= len(pages)

        current_page = pages[
            page_number
        ]

        y = content_top

        line_height = 38

        for line in current_page:

            draw.text(
                (
                    margin_x,
                    y
                ),
                line,
                font=text_font,
                fill=(225, 232, 240)
            )

            y += line_height


        # Page number

        page_text = (
            f"Page {page_number + 1} "
            f"of {len(pages)}"
        )

        draw.text(
            (
                margin_x,
                SCREEN_HEIGHT - 80
            ),
            page_text,
            font=small_font,
            fill=(100, 120, 140)
        )


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    footer = (
        "TimeFlow • "
        "Wallpaper automatically synced"
    )

    footer_bbox = draw.textbbox(
        (0, 0),
        footer,
        font=small_font
    )

    footer_width = (
        footer_bbox[2] -
        footer_bbox[0]
    )


    draw.text(
        (
            SCREEN_WIDTH -
            margin_x -
            footer_width,
            SCREEN_HEIGHT - 80
        ),
        footer,
        font=small_font,
        fill=(80, 100, 120)
    )


    # --------------------------------------------------------
    # SAVE IMAGE
    # --------------------------------------------------------

    WALLPAPER_DIR.mkdir(
        exist_ok=True
    )

    image.save(
        WALLPAPER_FILE,
        "PNG"
    )

    return WALLPAPER_FILE


# ============================================================
# SET DESKTOP WALLPAPER
# ============================================================

def set_wallpaper(image_path):
    """Set the generated image as the desktop wallpaper."""

    image_uri = (
        "file://"
        + str(image_path.resolve())
    )


    # GNOME / Ubuntu

    if shutil.which("gsettings"):

        success = False

        for setting in (
            "picture-uri",
            "picture-uri-dark"
        ):

            result = subprocess.run(
                [
                    "gsettings",
                    "set",
                    "org.gnome.desktop.background",
                    setting,
                    image_uri
                ],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            if result.returncode == 0:

                success = True


        if success:

            return True


    # Optional feh fallback

    if shutil.which("feh"):

        result = subprocess.run(
            [
                "feh",
                "--bg-scale",
                str(image_path)
            ],
            check=False
        )

        return result.returncode == 0


    return False


# ============================================================
# MAIN LOOP
# ============================================================

def main():

    print("=" * 60)

    print(
        "              TIMEFLOW WALLPAPER SYNC"
    )

    print("=" * 60)

    print()

    print(
        f"Watching : {TEXT_FILE}"
    )

    print(
        f"Screen   : {SCREEN_WIDTH}x{SCREEN_HEIGHT}"
    )

    print(
        f"Checking : every {CHECK_INTERVAL} second"
    )

    print()

    print(
        "Press Ctrl+C to stop."
    )

    print()


    last_modified = None

    last_content = None

    last_status = None

    current_page = 0

    last_page_change = time.monotonic()


    while True:

        # ----------------------------------------------------
        # Read file
        # ----------------------------------------------------

        content, status = read_text_file()


        # ----------------------------------------------------
        # Detect modification
        # ----------------------------------------------------

        try:

            modified = (
                TEXT_FILE.stat().st_mtime_ns
            )

        except FileNotFoundError:

            modified = None


        file_changed = (
            modified != last_modified
        )

        content_changed = (
            content != last_content
            or status != last_status
        )


        # ----------------------------------------------------
        # Change page periodically
        # ----------------------------------------------------

        now = time.monotonic()


        if (
            now - last_page_change
            >= PAGE_DURATION
        ):

            current_page += 1

            last_page_change = now


        # ----------------------------------------------------
        # Generate wallpaper
        #
        # It is regenerated every second so the clock
        # visibly updates in real time.
        # ----------------------------------------------------

        wallpaper = create_wallpaper(
            content,
            status,
            current_page
        )


        wallpaper_set = set_wallpaper(
            wallpaper
        )


        # ----------------------------------------------------
        # Print useful messages
        # ----------------------------------------------------

        current_timestamp = (
            datetime.now().strftime(
                "%H:%M:%S"
            )
        )


        if file_changed or content_changed:

            print(
                f"[{current_timestamp}] "
                "Text file changed -> "
                "wallpaper updated"
            )

        elif wallpaper_set:

            print(
                f"[{current_timestamp}] "
                "Clock updated"
            )

        else:

            print(
                f"[{current_timestamp}] "
                "Wallpaper generated"
            )


        # ----------------------------------------------------
        # Remember current state
        # ----------------------------------------------------

        last_modified = modified

        last_content = content

        last_status = status


        time.sleep(
            CHECK_INTERVAL
        )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()
        print("TimeFlow stopped.")