import textwrap

CHAPTER_GOALS = {
    1: textwrap.dedent("""\
        CHAPTER 1:
        Zae Hung, 19, found lifeless in her apartment on March 14, 2021.
        Coroner: Suicide by ligature hanging.

        Your Goal:
        """),
    2: textwrap.dedent("""\
        CHAPTER 2: 
        Find Zae’s hidden notes and clues about pressures she faced.
        """),
    3: textwrap.dedent("""\
        CHAPTER 3:
        Find Zae’s unsent letter about authenticity and burnout. 
        """),
    4: textwrap.dedent("""\
        CHAPTER 4:
        Locate files that reveal Zae’s last 48 hours.
        """),
    5: textwrap.dedent("""\
        CHAPTER 5: 
        Locate the final message that shows what really happened.
        """)
}

# sulod sa next.txt na file per chapter
STORY_CHUNKS = {
    1: textwrap.dedent("""\
        RECOVERED MESSAGE (fragmented):

        I am trying to be okay. I really am.
        I told Mom I would get help.
        But something happened yesterday.
        Something I cannot say out loud. 
        I feel watched. Followed. Misread.
        The truth is not in one file.
        It's scattered everywhere.
        -Zae
    """),
    2: textwrap.dedent("""\

        They said I deserve to disappear.
        Different accounts. Same words.
        -Zae
    """),
    3: textwrap.dedent("""\

        I don't hate life. I hate noise.
        The expectations.
        The perfect image.
        I lost control of my own voice.
        If something ever happens to me...
        please understand:
        It was slow.
        And no one ever noticed.
        -Zae
    """),
    4: textwrap.dedent("""\
        TIMELINE (recovered last 48 hours):

        - Tried to get help.
        - Attempted therapy.
        - Texted Mom emergency.
        - Went home early after disturbing anonymous message.
        - Laptop mid-upload. Music playing.
        - Anonymous messages continuing.
    """),
    5: textwrap.dedent("""\
        FINAL RECOVERY:

        Zae did not plan to die that night.
        Her laptop mid-upload. Music playing.
        Final message shows her crying silently, phone in hand.
        She tried to call someone. No one answered.

        Exhaustion led to her surrender.
        The world wouldn't listen.

        CASE CONCLUDED.
        THANK YOU FOR GIVING ZAE'S STORY THE VOICE SHE NEVER HAD.
    """)
}