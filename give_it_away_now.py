import datetime
import time
import getpass
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from colorama import init, Fore, Back, Style
from playsound import playsound

init(autoreset=True)
# add default options for chromedriver, this specifies to use mobile user-agent for easy loading.
opts = Options()
opts.add_argument(
    'user-agent=Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
# initialize chromedriver global variable.
chromedriver = None

# global element vars.
instant_box = 'box_click_target'
enter_button = 'enterSubmitForm'
enter_poll = 'enterPollButton'
tweet_id = 'ln_tw_tweet'
tweet_enter_id = 'ts_tw_tweet'
twitter_follow_id = 'lu_fo_follow'
twitter_follow_enter_id = 'ts_fo_follow'
next_button = '.a-last'
auth_error_message = 'auth-error-message-box'
auth_warning_message = 'auth-warning-message-box'

# global counter variables.
won_giveaways = 0
lost_giveaways = 0
entered_giveaways = 0
completed_giveaways = 0

# global functions
# boolean function to find if an element id exists.
def check_for_element_id(element_id):
    global chromedriver
    try:
        chromedriver.find_element_by_id(element_id)
        return True
    except:
        return False
# boolean function to find if a css selector exists.
def check_for_css_selector(css_selector):
    global chromedriver
    try:
        chromedriver.find_element_by_css_selector(css_selector)
        return True
    except:
        return False

# function to process the 'None' requirement giveaways.
def process_no_req_giveaways():
    global won_giveaways, lost_giveaways, entered_giveaways, completed_giveaways
    no_req_giveaways = chromedriver.find_elements_by_xpath('//div//span[contains(.,"None")]')
    number_of_no_req = str(len(no_req_giveaways))
    print(Fore.CYAN + Style.BRIGHT + "\n#### Number of 'None' Requirement GiveAways found on this page:  %s" % number_of_no_req)
    for ga in chromedriver.find_elements_by_xpath('//div//span[contains(.,"None")]'):
        new_tab = 1
        # For each prize criteria, open new Chrome tab and process the prize.
        chromedriver.execute_script("window.open('');")
        chromedriver.switch_to.window(chromedriver.window_handles[0])
        root_give_away = ga.find_element_by_xpath('./../..')
        # # print("\n" + root_give_away.text)
        get_url = root_give_away.find_element_by_link_text('View giveaway')
        href = get_url.get_attribute('href')

        chromedriver.switch_to.window(chromedriver.window_handles[new_tab])
        chromedriver.get(href)
        time.sleep(3)
        prize_name = chromedriver.find_element_by_id('prize-name').text
        prize_name = str(prize_name.encode('utf-8')).replace('"', "")
        
        is_instant = check_for_element_id(instant_box)
        is_enter = check_for_element_id(enter_button)
        
        print(Fore.WHITE + Style.BRIGHT + '\n**** Processing GiveAway for: %s' % prize_name)

        if is_instant is True and is_enter is False:
            giveaway_box = chromedriver.find_element_by_id(instant_box)
            giveaway_box.click()
            time.sleep(10)
            get_result = chromedriver.find_element_by_id('title')
            time.sleep(5)
            if "you didn't win" in get_result.text:
                lost_giveaways += 1
                print(Fore.YELLOW + Style.BRIGHT + '\n    **** You did not win: %s' % prize_name)
                time.sleep(5)
            elif "you're a winner!" in get_result.text:
                won_giveaways += 1
                print(Fore.GREEN + Style.BRIGHT + '\n    **** Winner Winner! Chicken Dinner!: %s' % prize_name)
                time.sleep(1)
                playsound('./sounds//btyswt.mp3')
                time.sleep(5)
            else:
                print(Fore.RED + Style.BRIGHT + '\n    ---- UNRECOGNIZED RESPONSE FOR: %s' % prize_name)
            chromedriver.close()
            chromedriver.switch_to.window(chromedriver.window_handles[0])
        elif is_instant is False and is_enter is True:
            enter_give_away = chromedriver.find_element_by_id(enter_button)
            enter_give_away.click()
            time.sleep(10)
            get_result = chromedriver.find_element_by_id('title')
            time.sleep(5)
            if "your entry has been received" in get_result.text:
                entered_giveaways += 1
                print(Fore.YELLOW + Style.BRIGHT + '\n    **** You have entered the GiveAway for: %s. You will receive an email if you won.' % prize_name)
                time.sleep(5)
            else:
                print "\nThis shouldn't happen.  RUN!"
            chromedriver.close()
            chromedriver.switch_to.window(chromedriver.window_handles[0])
        else:
            get_result = chromedriver.find_element_by_id('title')
            time.sleep(5)
            if "you didn't win" in get_result.text:
                completed_giveaways += 1
                print(Fore.YELLOW + Style.BRIGHT + '\n    **** You have already completed this GiveAway and you did not win.')
            elif "your entry has been received" in get_result.text:
                completed_giveaways += 1
                print(Fore.YELLOW + Style.BRIGHT + '\n    **** Your entry has already been received for this GiveAway.')
            else:
                print(Fore.RED + Style.BRIGHT + '\n    ---- Unrecognized error occured at getting GiveAway result.')
            chromedriver.close()
            chromedriver.switch_to.window(chromedriver.window_handles[0])

# function to process the 'Tweet' requirement giveaways.
def process_tweet_giveaways():
    global won_giveaways, lost_giveaways, entered_giveaways, completed_giveaways
    tweet_giveaways = chromedriver.find_elements_by_xpath('//div//span[contains(.,"Tweet a message")]')
    number_of_tweet_req = str(len(tweet_giveaways))
    print(Fore.CYAN + Style.BRIGHT + "\n#### Number of 'Tweet a message' Requirement GiveAways found on this page:  %s" % number_of_tweet_req)
    # print "\n#### Number of 'Tweet a message' Requirement GiveAways found on this page:  %s" % number_of_tweet_req
    for ga in chromedriver.find_elements_by_xpath('//div//span[contains(.,"Tweet a message")]'):
        new_tab = 1
        # For each prize criteria, open new Chrome tab and process the prize.
        chromedriver.execute_script("window.open('');")
        chromedriver.switch_to.window(chromedriver.window_handles[0])

        root_give_away = ga.find_element_by_xpath('./../..')
        # print("\n" + root_give_away.text)
        get_url = root_give_away.find_element_by_link_text('View giveaway')
        href = get_url.get_attribute('href')

        chromedriver.switch_to.window(chromedriver.window_handles[new_tab])
        chromedriver.get(href)
        time.sleep(3)
        prize_name = chromedriver.find_element_by_id('prize-name').text
        prize_name = str(prize_name.encode('utf-8')).replace('"', "")

        is_tweet = check_for_element_id(tweet_id)
        is_tweet_enter = check_for_element_id(tweet_enter_id)

        print(Fore.WHITE + Style.BRIGHT + '\n**** Processing GiveAway for: %s' % prize_name)

        if is_tweet is True and is_tweet_enter is False:
            tweet_button = chromedriver.find_element_by_id(tweet_id)
            tweet_button.click()
            time.sleep(5)
            
            # determine whether the tweet giveaway is instance or entered
            is_instant = check_for_element_id(instant_box)
            is_enter = check_for_element_id(enter_button)
        
            if is_instant is True and is_enter is False:
                giveaway_box = chromedriver.find_element_by_id(instant_box)
                giveaway_box.click()
                time.sleep(10)
                get_result = chromedriver.find_element_by_id('title')
                time.sleep(5)
                if "you didn't win" in get_result.text:
                    lost_giveaways += 1
                    print(Fore.YELLOW + Style.BRIGHT + '\n    **** You did not win: %s' % prize_name)
                    time.sleep(5)
                elif "you're a winner!" in get_result.text:
                    won_giveaways += 1
                    print(Fore.GREEN + Style.BRIGHT + '\n    **** Winner Winner! Chicken Dinner!: %s' % prize_name)
                    time.sleep(1)
                    playsound('./sounds//btyswt.mp3')
                    time.sleep(5)
                else:
                    print(Fore.RED + Style.BRIGHT + '\n    ---- UNRECOGNIZED RESPONSE FOR: %s' % prize_name)
                chromedriver.close()
                chromedriver.switch_to.window(chromedriver.window_handles[0])
            elif is_instant is False and is_enter is True:
                enter_give_away = chromedriver.find_element_by_id(enter_button)
                enter_give_away.click()
                time.sleep(10)
                get_result = chromedriver.find_element_by_id('title')
                time.sleep(5)
                if "your entry has been received" in get_result.text:
                    entered_giveaways += 1
                    print(Fore.YELLOW + Style.BRIGHT + '\n    **** You have entered the GiveAway for: %s. You will receive an email if you won.' % prize_name)
                else:
                    print "\nThis shouldn't happen.  RUN!"
                chromedriver.close()
                chromedriver.switch_to.window(chromedriver.window_handles[0])
            else:
                get_result = chromedriver.find_element_by_id('title')
                time.sleep(5)
                if "you didn't win" in get_result.text:
                    completed_giveaways += 1
                    print(Fore.YELLOW + Style.BRIGHT + '\n    **** You have already completed this GiveAway and you did not win.')
                else:
                    print(Fore.RED + Style.BRIGHT + '\n    ---- Your Twitter account may not be authorized with Amazon.')
                chromedriver.close()
                chromedriver.switch_to.window(chromedriver.window_handles[0])
        elif is_tweet_enter is True and is_tweet is False:
            tweet_enter_button = chromedriver.find_element_by_id(tweet_enter_id)
            tweet_enter_button.click()
            time.sleep(5)
            
            # determine whether the tweet giveaway is instance or entered
            is_instant = check_for_element_id(instant_box)
            is_enter = check_for_element_id(enter_button)
        
            if is_instant is True and is_enter is False:
                giveaway_box = chromedriver.find_element_by_id(instant_box)
                giveaway_box.click()
                time.sleep(10)
                get_result = chromedriver.find_element_by_id('title')
                time.sleep(5)
                if "you didn't win" in get_result.text:
                    lost_giveaways += 1
                    print(Fore.YELLOW + Style.BRIGHT + '\n    **** You did not win: %s' % prize_name)
                    time.sleep(5)
                elif "you're a winner!" in get_result.text:
                    won_giveaways += 1
                    print(Fore.GREEN + Style.BRIGHT + '\n    **** Winner Winner! Chicken Dinner!: %s' % prize_name)
                    time.sleep(1)
                    playsound('./sounds//btyswt.mp3')
                    time.sleep(5)
                else:
                    get_result = chromedriver.find_element_by_id('title')
                    time.sleep(5)
                    if "you didn't win" in get_result.text:
                        completed_giveaways += 1
                        print(Fore.YELLOW + Style.BRIGHT + '\n    **** You have already completed this GiveAway and you did not win.')
                    else:
                        print(Fore.RED + Style.BRIGHT + '\n    ---- Your Twitter account may not be authorized with Amazon.')
                chromedriver.close()
                chromedriver.switch_to.window(chromedriver.window_handles[0])
            elif is_instant is False and is_enter is True:
                enter_give_away = chromedriver.find_element_by_id(enter_button)
                enter_give_away.click()
                time.sleep(10)
                get_result = chromedriver.find_element_by_id('title')
                time.sleep(5)
                if "your entry has been received" in get_result.text:
                    entered_giveaways += 1
                    print(Fore.YELLOW + Style.BRIGHT + '\n    **** You have entered the GiveAway for: %s. You will receive an email if you won.' % prize_name)
                else:
                    print "\nThis shouldn't happen.  RUN!"
                chromedriver.close()
                chromedriver.switch_to.window(chromedriver.window_handles[0])
            else:
                get_result = chromedriver.find_element_by_id('title')
                time.sleep(5)
                if "you didn't win" in get_result.text:
                    completed_giveaways += 1
                    print(Fore.YELLOW + Style.BRIGHT + '\n    **** You have already completed this GiveAway and you did not win.')
                elif "your entry has been received" in get_result.text:
                    completed_giveaways += 1
                    print(Fore.YELLOW + Style.BRIGHT + '\n    **** Your entry has already been received for this GiveAway.')
                else:
                    print(Fore.RED + Style.BRIGHT + '\n    ---- Your Twitter account may not be authorized with Amazon.')
                chromedriver.close()
                chromedriver.switch_to.window(chromedriver.window_handles[0])
        else:
            get_result = chromedriver.find_element_by_id('title')
            time.sleep(5)
            if "you didn't win" in get_result.text:
                completed_giveaways += 1
                print(Fore.YELLOW + Style.BRIGHT + '\n    **** You have already completed this GiveAway and you did not win.')
            elif "your entry has been received" in get_result.text:
                completed_giveaways += 1
                print(Fore.YELLOW + Style.BRIGHT + '\n    **** Your entry has already been received for this GiveAway.')
            else:
                print(Fore.RED + Style.BRIGHT + '\n    ---- Your Twitter account may not be authorized with Amazon.')
            chromedriver.close()
            chromedriver.switch_to.window(chromedriver.window_handles[0])

# function to process the 'Twitter Follow' requirement giveaways.
def process_twitter_follow_giveaways():
    global won_giveaways, lost_giveaways, entered_giveaways, completed_giveaways
    twitter_follow_giveaways = chromedriver.find_elements_by_xpath('//div//span[contains(.,"on Twitter")]')
    number_of_twitter_follow_req = str(len(twitter_follow_giveaways))
    print(Fore.CYAN + Style.BRIGHT + "\n#### Number of 'Follow on Twitter' Requirement GiveAways found on this page:  %s" % number_of_twitter_follow_req)
    for ga in chromedriver.find_elements_by_xpath('//div//span[contains(.,"on Twitter")]'):
        new_tab = 1
        # For each prize criteria, open new Chrome tab and process the prize.
        chromedriver.execute_script("window.open('');")
        chromedriver.switch_to.window(chromedriver.window_handles[0])

        root_give_away = ga.find_element_by_xpath('./../..')
        # print("\n" + root_give_away.text)
        get_url = root_give_away.find_element_by_link_text('View giveaway')
        href = get_url.get_attribute('href')

        chromedriver.switch_to.window(chromedriver.window_handles[new_tab])
        chromedriver.get(href)
        time.sleep(3)
        prize_name = chromedriver.find_element_by_id('prize-name').text
        prize_name = str(prize_name.encode('utf-8')).replace('"', "")

        is_twitter_follow = check_for_element_id(twitter_follow_id)
        is_twitter_follow_enter = check_for_element_id(twitter_follow_enter_id)

        print(Fore.WHITE + Style.BRIGHT + '\n**** Processing GiveAway for: %s' % prize_name)

        if is_twitter_follow is True and is_twitter_follow_enter is False:
            twitter_follow_button = chromedriver.find_element_by_id(twitter_follow_id)
            twitter_follow_button.click()
            time.sleep(5)
            # determine whether the tweet giveaway is instance or entered
            is_instant = check_for_element_id(instant_box)
            is_enter = check_for_element_id(enter_button)
        
            if is_instant is True and is_enter is False:
                giveaway_box = chromedriver.find_element_by_id(instant_box)
                giveaway_box.click()
                time.sleep(10)
                get_result = chromedriver.find_element_by_id('title')
                time.sleep(5)
                if "you didn't win" in get_result.text:
                    lost_giveaways += 1
                    print(Fore.YELLOW + Style.BRIGHT + '\n    **** You did not win: %s' % prize_name)
                    time.sleep(5)
                elif "you're a winner!" in get_result.text:
                    won_giveaways += 1
                    print(Fore.GREEN + Style.BRIGHT + '\n    **** Winner Winner! Chicken Dinner!: %s' % prize_name)
                    time.sleep(1)
                    playsound('./sounds//btyswt.mp3')
                    time.sleep(5)
                else:
                    print(Fore.RED + Style.BRIGHT + '\n    ---- UNRECOGNIZED RESPONSE FOR: %s' % prize_name)
                chromedriver.close()
                chromedriver.switch_to.window(chromedriver.window_handles[0])
            elif is_instant is False and is_enter is True:
                enter_give_away = chromedriver.find_element_by_id(enter_button)
                enter_give_away.click()
                time.sleep(10)
                get_result = chromedriver.find_element_by_id('title')
                time.sleep(5)
                if "your entry has been received" in get_result.text:
                    entered_giveaways += 1
                    print(Fore.YELLOW + Style.BRIGHT + '\n    **** You have entered the GiveAway for: %s. You will receive an email if you won.' % prize_name)
                else:
                    print "\nThis shouldn't happen.  RUN!"
                chromedriver.close()
                chromedriver.switch_to.window(chromedriver.window_handles[0])
            else:
                get_result = chromedriver.find_element_by_id('title')
                time.sleep(5)
                if "you didn't win" in get_result.text:
                    completed_giveaways += 1
                    print(Fore.YELLOW + Style.BRIGHT + '\n    **** You have already completed this GiveAway and you did not win.')
                elif "your entry has been received" in get_result.text:
                    completed_giveaways += 1
                    print(Fore.YELLOW + Style.BRIGHT + '\n    **** Your entry has already been received for this GiveAway.')
                else:
                    print(Fore.RED + Style.BRIGHT + '\n    ---- Your Twitter account may not be authorized with Amazon.')
                chromedriver.close()
                chromedriver.switch_to.window(chromedriver.window_handles[0])
        elif is_twitter_follow_enter is True and is_twitter_follow is False:
            twitter_follow_enter_button = chromedriver.find_element_by_id(twitter_follow_enter_id)
            twitter_follow_enter_button.click()
            time.sleep(5)
            
            # determine whether the tweet giveaway is instance or entered
            is_instant = check_for_element_id(instant_box)
            is_enter = check_for_element_id(enter_button)
        
            if is_instant is True and is_enter is False:
                giveaway_box = chromedriver.find_element_by_id(instant_box)
                giveaway_box.click()
                time.sleep(10)
                get_result = chromedriver.find_element_by_id('title')
                time.sleep(5)
                if "you didn't win" in get_result.text:
                    lost_giveaways += 1
                    print(Fore.YELLOW + Style.BRIGHT + '\n    **** You did not win: %s' % prize_name)
                    time.sleep(5)
                elif "you're a winner!" in get_result.text:
                    won_giveaways += 1
                    print(Fore.GREEN + Style.BRIGHT + '\n    **** Winner Winner! Chicken Dinner!: %s' % prize_name)
                    time.sleep(1)
                    playsound('./sounds//btyswt.mp3')
                    time.sleep(5)
                else:
                    print(Fore.RED + Style.BRIGHT + '\n    ---- UNRECOGNIZED RESPONSE FOR: %s' % prize_name)
                chromedriver.close()
                chromedriver.switch_to.window(chromedriver.window_handles[0])
            elif is_instant is False and is_enter is True:
                enter_give_away = chromedriver.find_element_by_id(enter_button)
                enter_give_away.click()
                time.sleep(10)
                get_result = chromedriver.find_element_by_id('title')
                time.sleep(5)
                if "your entry has been received" in get_result.text:
                    entered_giveaways += 1
                    print(Fore.YELLOW + Style.BRIGHT + '\n    **** You have entered the GiveAway for: %s. You will receive an email if you won.' % prize_name)
                else:
                    print(Fore.RED + Style.BRIGHT + '\n    ---- You have already completed this GiveAway or your Twitter account is not authorized to complete GiveAways with Amazon.')
                chromedriver.close()
                chromedriver.switch_to.window(chromedriver.window_handles[0])
            else:
                get_result = chromedriver.find_element_by_id('title')
                time.sleep(5)
                if "you didn't win" in get_result.text:
                    completed_giveaways += 1
                    print(Fore.YELLOW + Style.BRIGHT + '\n    **** You have already completed this GiveAway and you did not win.')
                elif "your entry has been received" in get_result.text:
                    completed_giveaways += 1
                    print(Fore.YELLOW + Style.BRIGHT + '\n    **** Your entry has already been received for this GiveAway.')
                else:
                    print(Fore.RED + Style.BRIGHT + '\n    ---- Your Twitter account may not be authorized with Amazon.')
                chromedriver.close()
                chromedriver.switch_to.window(chromedriver.window_handles[0])
        else:
            get_result = chromedriver.find_element_by_id('title')
            time.sleep(5)
            if "you didn't win" in get_result.text:
                completed_giveaways += 1
                print(Fore.YELLOW + Style.BRIGHT + '\n    **** You have already completed this GiveAway and you did not win.')
            elif "your entry has been received" in get_result.text:
                completed_giveaways += 1
                print(Fore.YELLOW + Style.BRIGHT + '\n    **** Your entry has already been received for this GiveAway.')
            else:
                print(Fore.RED + Style.BRIGHT + '\n    ---- Your Twitter account may not be authorized with Amazon.')
            chromedriver.close()
            chromedriver.switch_to.window(chromedriver.window_handles[0])
# main method
def main():
    # use the global chromedriver variable.
    global chromedriver
    # start at page 1 of Giveaways.
    page_count = 1
    # user email and password inputs.
    user_email_input = raw_input("Enter your Amazon email address: ")
    user_password_input = getpass.getpass("Enter your Amazon password: ")
    # launch chromedriver with opts args.
    chromedriver = webdriver.Chrome('/Users/zack/PycharmProjects/chromedriver', chrome_options=opts)
    # navigate to Amazon sign-in page with redirect to the Giveaway homepage.
    chromedriver.get(
        'https://www.amazon.com/ap/signin?_encoding=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fga%2Fgiveaways')
    time.sleep(1)
    # time stamp for log file
    time_stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    print(Fore.CYAN + Style.BRIGHT + "\nLogging into Amazon..."),
    # Amazon account login
    email = chromedriver.find_element_by_name('email')
    email.send_keys(user_email_input)
    password = chromedriver.find_element_by_name('password')
    password.send_keys(user_password_input)
    grab_checkboxes = chromedriver.find_elements_by_css_selector('.a-icon.a-icon-checkbox')
    keep_signed_in = grab_checkboxes[1]
    keep_signed_in.click()
    sign_in_submit = chromedriver.find_element_by_id('signInSubmit')
    sign_in_submit.click()
    time.sleep(3)

    is_login_error = check_for_element_id(auth_error_message)
    is_login_warning = check_for_element_id(auth_warning_message)

    if is_login_error is True:
        print(Fore.RED + Style.BRIGHT + "Login Unsuccessful!  Exiting...")
        time.sleep(1)
        playsound('./sounds//fr.mp3')
        chromedriver.quit()
        exit(1)
    elif is_login_warning is True:
        print(Fore.YELLOW + Style.BRIGHT + "Login Unsuccessful!  Enter credentials with Captcha or script will exit...")
        time.sleep(60)
        # playsound('.\sounds\\fr.mp3')
        chromedriver.quit()
        exit(1)
    else:
        print(Fore.GREEN + Style.BRIGHT + "Login Successful!  Continuing...")
    time.sleep(5)

    is_next = check_for_css_selector(next_button)
    while is_next is True:
        print(Fore.CYAN + Style.BRIGHT + '\nProcessing GiveAways for Page: %s' % page_count)
        process_no_req_giveaways()
        process_tweet_giveaways()
        process_twitter_follow_giveaways()
        chromedriver.switch_to.window(chromedriver.window_handles[0])
        next_page = chromedriver.find_element_by_css_selector(next_button)
        next_page.click()
        page_count += 1
        is_next = check_for_css_selector(next_button)
    chromedriver.switch_to.window(chromedriver.window_handles[0])

    # derived totals from global counter variables
    instant_giveaways = won_giveaways + lost_giveaways
    all_giveaways = instant_giveaways + entered_giveaways + completed_giveaways

    print "\n**** Script completed ****"
    print "\nTotal won: %d" % won_giveaways
    print "\nTotal lost: %d" % lost_giveaways
    print "\nTotal entry giveaways: %d" % entered_giveaways
    print "\nTotal instant giveaways: %d" % instant_giveaways
    print "\nAlready completed giveaways: %d" % completed_giveaways
    print "\nALL giveaways: %d" % all_giveaways
    exit(0)

# process main method call
if __name__ == '__main__':
    main()
