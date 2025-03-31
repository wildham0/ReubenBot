def print_help():
    help_text = ("ReubenBot has 3 primary uses.\n\n" +
                "Use `/addrole` and `/removerole` to self-assign roles. For a list of self-assignable roles, use `/listroles`.\n\n" +
                "Use `/startstreaming` to be listed in the user panel as Now streaming FFMQ. This should be used only when streaming FFMQ or FFMQR.\n" +
                "Ask @moderation if you're not sure. You can use `/stopstreaming` when you're done or set a number of hours with `/startstreaming`.\n\n" +
                "Use `/submit`, `/forfeit` or `/spectate` to participate to the weekly seed in #weekly-seed.")
    return help_text

def print_roles():
    role_text = ("The following servers roles can be requested; use the `/addrole` command to do so.\n\n" +
                "`weeklies racer`: Get this role to be informed when a new weekly async seed is posted.\n" +
                "`monthlies racer`: Get this role to be pinged the day of the monthly community race.\n" +
                "`ping me to race`: Get this role to be pinged when someone else is interested to race.\n" +
                "`ping me to ap`: Get this role to be pinged when someone wants to run an Archipelago game.\n" +
                "`broadcast team`: Get this role to be pinged when an event (races, marathon submissions, etc.) needs help for broadcasting; common roles are restreamer, commentator and tracker.")
    return role_text
