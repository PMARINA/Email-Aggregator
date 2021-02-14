from Event import event


def get_email(event, occ):
    body = """
    <div dir="ltr">
        <div class="gmail_quote">
            <div dir="ltr">
                <div class="gmail_quote">
                    <div dir="ltr">
                        <div style="text-align:center"><img src="https://i.postimg.cc/sx8hCztQ/big-logo.png" alt="CTC Logo"
                                width="398" height="143"><br>
                        </div>
                        <div style="text-align:center"><b>Hi Everyone!</b></div>
                        <div style="text-align:center"><br></div>
"""
    body += f"""
                        <div style="text-align:center">This is a reminder that {event.name} will happening today, {event.get_date_time_strings([occ])[0]} at the following Zoom link.
                        </div>
                        <div style="text-align:center"><a
                                href="https://stevens.zoom.us/s/91570444680">https://stevens.zoom.us/s/<wbr>91570444680</a>
                        </div>
                    </div>
                    <div style="text-align:center">Hope to see you there!</div>
                </div>
            </div>
        </div>
    </div>
    </div>
"""
    return body


def write_email(event, occ):
    body = get_email(event, occ)
    with open("Output.html", "w") as output:
        output.write(body)
    return body


# if __name__ == "__main__":
#     write_email(None, None)
