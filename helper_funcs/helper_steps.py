#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" STEP FIVE """

import logging


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
LOGGER = logging.getLogger(__name__)


def parse_to_meaning_ful_text(input_phone_number, in_dict):
    """ convert the dictionary returned in STEP FOUR
    into Telegram HTML text """
    me_t = ""
    me_t += "<i>Phone Number</i>: "
    me_t += f"<u>{input_phone_number}</u>"
    me_t += "\n"
    me_t += "\n"
    me_t += "<i>App Configuration</i>"
    me_t += "\n"
    me_t += "<b>APP ID</b>: "
    me_t += "<code>{}</code>".format(in_dict["App Configuration"]["app_id"])
    me_t += "\n"
    me_t += "<b>API HASH</b>: "
    me_t += "<code>{}</code>".format(in_dict["App Configuration"]["api_hash"])
    me_t += "\n"
    me_t += "\n"
    me_t += "<i>Available MTProto Servers</i>"
    me_t += "\n"
    me_t += "<b>Production Configuration</b>: "
    me_t += "<code>{}</code> <u>{}</u>".format(
        in_dict["Available MTProto Servers"]["production_configuration"]["IP"],
        in_dict["Available MTProto Servers"]["production_configuration"]["DC"]
    )
    me_t += "\n"
    me_t += "<b>Test Configuration</b>: "
    me_t += "<code>{}</code> <u>{}</u>".format(
        in_dict["Available MTProto Servers"]["test_configuration"]["IP"],
        in_dict["Available MTProto Servers"]["test_configuration"]["DC"]
    )
    me_t += "\n"
    me_t += "\n"
    me_t += "<i>Disclaimer</i>: "
    me_t += "<u>{}</u>".format(
        in_dict["Disclaimer"]
    )
    return me_t


def extract_code_imn_ges(ptb_message):
    """ extracts the input message, and returns the
    Telegram Web login code"""
    # initialize a variable that can be used
    # to store the web login code after a
    # sequence of conditionals
    telegram__web_login_code = None
    # the original message text sent by the user
    incoming_message_text = ptb_message.text
    # lower case can be used as a helper in the
    # comparison logic
    # N.B.: the PASSWORD is case sensitive,
    # so, "telegram__web_login_code" should have the original text,
    # without conversion
    incoming_message_text_in_lower_case = incoming_message_text.lower()
    if "web login code" in incoming_message_text_in_lower_case:
        parted_message_pts = incoming_message_text.split("\n")
        # this logic is deduced by Trial and Error
        if len(parted_message_pts) >= 2:
            telegram__web_login_code = parted_message_pts[1]
            # there might be a better way, but 😐😪😪
    elif "\n" in incoming_message_text_in_lower_case:
        # this condition ideally, should not occur,
        LOGGER.info("did it come inside this 'elif' ?")
    else:
        telegram__web_login_code = incoming_message_text
    return telegram__web_login_code


def get_phno_imn_ges(ptb_message):
    """ gets the phone number (in international format),
    from the input message"""
    LOGGER.info(ptb_message)
    my_telegram_ph_no = None
    if ptb_message.text is not None:
        if len(ptb_message.entities) > 0:
            for c_entity in ptb_message.entities:
                if c_entity.type == "phone_number":
                    my_telegram_ph_no = ptb_message.text[
                        c_entity.offset:c_entity.length
                    ]
        else:
            my_telegram_ph_no = ptb_message.text
    elif ptb_message.contact is not None:
        # https://archive.is/X4gsK
        if ptb_message.contact.phone_number != "":
            my_telegram_ph_no = ptb_message.contact.phone_number
    return my_telegram_ph_no


def compareFiles(first, second):
    """ this code was copied
    line for line from
    https://github.com/DrKLO/Telegram/blob/7fb9f0b85621940e0a5ba977278f6f27fc323046/apkdiff.py#L4
    """
    while True:
        firstBytes = first.read(4096)
        secondBytes = second.read(4096)
        if firstBytes != secondBytes:
            return False
        if firstBytes == b"":
            break
    return True


