


TEXT_HELP = """This is my personal bot with my comic (maybe not) projects

<b>commands:</b>
    Video from youtube to tg circle: 
        !vtc [LINK] [START] [DURATION]
"""

TEXTS_HELP_COMMANDS = {
    "vtc":
        """!vtc [LINK] [START] [DURATION]
        
        [START]
            format: 00:00:00 (hour:minute:second) 
            This is the time from which the circle will be recorded.
        [DURATION] 
            format: 00 (seconds) 
            This is the duration of the circle
        
        example:
            !vtc https://www.youtube.com/watch?v=P-kXwwKnzfY 00:00:03 3

        you have use !vtccorp to get a cropped video
        """
}