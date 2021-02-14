from loguru import logger
import inflect
import Event

p = inflect.engine()

# def get_email(event_list):
#     message = """
#     <div dir="ltr">
#     <div style="text-align:center"><img src="https://i.postimg.cc/sx8hCztQ/big-logo.png" alt="CTC Logo" width="398" height="143"><br><br></div>
#     <div>
#         <div style="text-align:center"><b>Hi Everyone!</b></div>
#         <div style="text-align:center"><b><br></b></div>
#     """
#     message += """
#         <div style="text-align:center"><b>Our event this week is Intro to KiCad.</b></div>
#         <div style="text-align:center">KiCad is a free PCB design software used in industry to develop and manufacture circuit boards. It's useful for both professional and hobbyist circuit development.</div>
#         <div style="text-align:center"><a href="https://stevensctc.page.link/SignUp-2020-IntroKiCad" target="_blank" data-saferedirecturl="https://www.google.com/url?hl=en&amp;q=https://stevensctc.page.link/SignUp-2020-IntroKiCad&amp;source=gmail&amp;ust=1613415193791000&amp;usg=AFQjCNGL8rnrt5cOeCyf5rmCgmZPma6ejw">Sign Up!</a></div>
#         <div style="text-align:center">Thursday, December 3rd, 2020 (12/03/2020) at 9 PM Eastern - Intro to KiCad: <a href="https://stevensctc.page.link/zoom" target="_blank" data-saferedirecturl="https://www.google.com/url?hl=en&amp;q=https://stevensctc.page.link/zoom&amp;source=gmail&amp;ust=1613415193791000&amp;usg=AFQjCNG8AaHuPgaKNpzznRJMp1IvetVE_g">https://stevensctc.page.link/<wbr>zoom</a></div>
#     </div>
#     <div style="text-align:center">Hope to see you there!</div>
#     <div style="text-align:center"><br></div>
#     <div style="text-align:center">If&nbsp;you have any questions please feel free to reach out to us at this email and follow us on Instagram to stay up to date with announcements&nbsp;and future events.</div>
#     <div style="text-align:center">
#         <div><img src="?ui=2&amp;ik=d3ec2f591d&amp;view=fimg&amp;th=177a1e339d3fab8e&amp;attid=0.2&amp;disp=emb&amp;realattid=ii_177a1e1a79b2ca73e062&amp;attbid=ANGjdJ9OreYAFQdNJXoNCkUeFWD4kCr2ZF-KbSVgVmqxJta7bVRFUIi5PW5kscMRzYl8xbR-_N4DXdWe6_prOqmutH6tSjmy-jfmMQqMQBODfnTXhTJdT4U4v6s3n2k&amp;sz=w70-h70&amp;ats=1613328793791&amp;rm=177a1e339d3fab8e&amp;zw&amp;atsh=1" alt="Screen Shot 2020-08-29 at 10.14.40 PM.png" width="35" height="35"><img src="?ui=2&amp;ik=d3ec2f591d&amp;view=fimg&amp;th=177a1e339d3fab8e&amp;attid=0.3&amp;disp=emb&amp;realattid=ii_177a1e1a79b2a727a553&amp;attbid=ANGjdJ88GR-7mOOAgs1NKAHtoVjQmCeYJYEZmGbvgS_DM3WJPC_7WeLax_gxGHVv_qGKrg94aYs0ou3dBv_fiU2FR4nXAzUZVBLBh-ZcTKpx1tuO-4dSvoFV6Gc32Co&amp;sz=w60-h72&amp;ats=1613328793791&amp;rm=177a1e339d3fab8e&amp;zw&amp;atsh=1" alt="Screen Shot 2020-09-06 at 6.31.36 PM.png" width="30" height="36"><img src="?ui=2&amp;ik=d3ec2f591d&amp;view=fimg&amp;th=177a1e339d3fab8e&amp;attid=0.4&amp;disp=emb&amp;realattid=ii_177a1e1a79cc231a2be4&amp;attbid=ANGjdJ-9n8wmaI2_KUc5BH42dO00mUcFDMlaS9s-VRYQJesKSI57EX02VROnVFgcuTugFHCwyiFWswJoLL1FPdvmRpmcipgr0e8QALitn6Smhvd7CxAihw7dO3TzSmY&amp;sz=w280-h72&amp;ats=1613328793791&amp;rm=177a1e339d3fab8e&amp;zw&amp;atsh=1" alt="Screen Shot 2020-09-06 at 6.29.58 PM.png" width="140" height="36"><img src="?ui=2&amp;ik=d3ec2f591d&amp;view=fimg&amp;th=177a1e339d3fab8e&amp;attid=0.5&amp;disp=emb&amp;realattid=ii_177a1e1a79d2ca73e065&amp;attbid=ANGjdJ9jpO5kf0AgfjQ650V96jw3qtGp2GwXKSlY9Pb8tnr07IoqcympqUgPItcWIQnaQAMolLCqEde32zpeUmQQOS8pJ8qyyaN7U9yBNuECjm-vfRl8oKerbebzukU&amp;sz=w74-h76&amp;ats=1613328793791&amp;rm=177a1e339d3fab8e&amp;zw&amp;atsh=1" alt="Screen Shot 2020-08-29 at 10.14.40 PM.png" width="37" height="38"></div>
#         <div><br></div>
#         <div>Join our slack for important announcements&nbsp;about events, to ask questions about previous events, and access instructors directly</div>
#         <div><a href="https://stevensctc.page.link/slack" target="_blank" data-saferedirecturl="https://www.google.com/url?hl=en&amp;q=https://stevensctc.page.link/slack&amp;source=gmail&amp;ust=1613415193791000&amp;usg=AFQjCNEZuwp-S1QtGgY_i_g1OJRUz-8JRw">https://stevensctc.page.link/<wbr>slack</a></div>
#         <div><br></div>
#         <div>Want to know more? Check out our website for info on who we are, all event sign-ups, contact information, and to meet your instructors!&nbsp;</div>
#         <div><a href="https://stevensctc.page.link/home" target="_blank" data-saferedirecturl="https://www.google.com/url?hl=en&amp;q=https://stevensctc.page.link/home&amp;source=gmail&amp;ust=1613415193791000&amp;usg=AFQjCNEvXIASco2nRQfvNXbS89A29UHRiw">https://stevensctc.page.link/<wbr>home</a><br></div>
#     </div>
#     <div style="text-align:center"><br></div>
#     <div style="text-align:center">Another reminder to please use our website to sign up for upcoming events here: <a href="https://stevensctc.page.link/events" target="_blank" data-saferedirecturl="https://www.google.com/url?hl=en&amp;q=https://stevensctc.page.link/events&amp;source=gmail&amp;ust=1613415193791000&amp;usg=AFQjCNEHsWbnaoR1f9DDedXqhIAtdlR0lA">Sign Up!</a></div>
#     </div>
#     """
def get_email(event_list):
    preamble = """
                    <div style="text-align:center"><img
                            src="https://i.postimg.cc/sx8hCztQ/big-logo.png"
                            alt="CTC Logo" width="398" height="143"><br>
                    </div>
                    <div>
                        <div style="text-align:center"><b>Hi Everyone!</b></div>
                        <div style="text-align:center"><br></div>
                """

    message = preamble
    if len(event_list) > 1:
        for event_number in range(len(event_list)):
            # for s in event.get_date_time_strings():
            #     logger.debug(s)
            event = event_list[event_number]
            s = event.get_date_time_strings()[0]
            message += f"""
                            <div style="text-align:center"><b>Our {p.number_to_words(p.ordinal(event_number+1))} event this week is {event.name}</b></div>
                            <div style="text-align:center">{event.description}</div>
                            <div style="text-align:center">{s} - <a
                                    href="https://stevensctc.page.link/zoom">stevensctc.page.link/zoom</a>
                            <div style="text-align:center"><a href="{event.sign_up_url}">Sign Up!</a></div>
                            </div>
                        """
    else:
        event = event_list[0]
        s = event.get_date_time_strings()[0]
        message += f"""
                        <div style="text-align:center"><b>This week's event is {event.name}</b></div>
                        <div style="text-align:center">{event.description}</div>
                        <div style="text-align:center">{s} - <a
                                href="https://stevensctc.page.link/zoom">stevensctc.page.link/zoom</a>
                        <div style="text-align:center"><a href="{event.sign_up_url}">Sign Up!</a></div>
                        </div>
                    """
    # The footer of the email
    message += """
                    <div style="text-align:center">Hope to see you there!</div>
                    <div style="text-align:center"><br></div>
                    <div style="text-align:center">If you have any questions please feel free to reach out to us at this email and follow us on Instagram to stay up to date with announcements and future events.</div>
                    <div style="text-align:center">
                    <div><img src="https://i.postimg.cc/25pVx2DY/logo.png"
                        alt="Small Logo" width="35" height="35"><img
                        src="https://i.postimg.cc/435sh54B/atsign.png"
                        alt="Instagram Atsign" width="30" height="36"><img
                        src="https://i.postimg.cc/tgwQ6MQd/ctc-insta-handle.png"
                        alt="Insta Handle" width="140" height="36"><img
                        src="https://i.postimg.cc/25pVx2DY/logo.png"
                        alt="Small Logo" width="35" height="35">
                    </div>
                    <div><br></div>
                    <div>Join our slack for important announcements about events, to ask questions about previous events, and access instructors directly </div>
                        <div><a href="https://stevensctc.page.link/slack">stevensctc.page.link/slack</a></div>
                        <div><br></div>
                        <div>Want to know more? Check out our website for info on who we are, all event sign-ups, contact information, and to meet your instructors! </div>
                        <div><a href="https://stevensctc.page.link/home" >https://stevensctc.page.link/home</a><br></div>
                    </div>
                    <div style="text-align:center"><br></div>
                    <div style="text-align:center">Please use our website to sign up for upcoming events here: <a href="https://stevensctc.page.link/events" >Sign Up!</a></div>
                    </div>
                """
    return message


def write_email(event_list):
    body = get_email(event_list)
    with open("Output.html", "w+") as output:
        output.write(body)
    return body


if __name__ == "__main__":
    write_email([])
