def make_summary(user_choices, risk1, risk2, utility):
    msg = "<h3>SAFE DATA TOOL REPORT</h3>"
    msg += "<b>User Choices:</b> " + str(user_choices) + "<br><hr>"
    msg += f"<b>Risk - Before:</b> {risk1}<br><b>Risk - After:</b> {risk2}<hr>"
    msg += "<b>Utility (KS tests):</b> " + str(utility) + "<hr>"
    return msg
