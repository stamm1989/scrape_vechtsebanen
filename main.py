  
import datetime
import json
import logging
logging.basicConfig(format='[%(asctime)s, %(name)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger=logging.getLogger(__name__)
import os
import re
import time
from glob import glob
from shutil import move

import pandas as pd
import pretty_html_table
import requests
import sendmail
import yaml
import send_mail

def fetch_open_tickets(date_from, date_to):

    date_range = pd.date_range(start=date_from, end=date_to)

    # init session
    session = requests.session()
    resp = session.get('https://vechtsebanen.nl/')

    def fetch_timeslots(reservation_date):

        s_date = reservation_date.strftime('%Y-%m-%d')
        logger.info(f'Fetching {s_date}')

        resp = session.get(f'https://vechtsebanen.nl/Website.Api/Access/Tickets?&date={s_date}')
        dct_data = resp.json()

        pd_data = None

        if dct_data['response'] is not None:
            pd_data = pd.DataFrame(dct_data['response'])
            pd_data['dateSlot'] = reservation_date

        return pd_data

    # reservation_date = date_range[15]
    l_timeslots = [fetch_timeslots(res_date) for res_date in date_range]

    pd_timeslots = pd.concat(l_timeslots).reset_index(drop=True)

    # Remove irrelivant timeslots
    l_not_availble = pd_timeslots[pd_timeslots['restCount'] <= 0].index
    pd_timeslots.drop(l_not_availble, inplace=True)

    l_relevant_timeslot = pd_timeslots[~pd_timeslots['timeFrom'].isin(['19:30:00', '21:15:00'])].index
    pd_timeslots.drop(l_relevant_timeslot, inplace=True)

    l_relevant_ticket_type = pd_timeslots[pd_timeslots['articleId'] != 6].index
    pd_timeslots.drop(l_relevant_ticket_type, inplace=True)

    return pd_timeslots


def main():
    date_from = datetime.datetime.now().date()
    date_to = (datetime.datetime.now() + datetime.timedelta(days=21)).date()

    pd_timeslots = fetch_open_tickets(date_from, date_to)

    # Drop non relevant column
    pd_timeslots.drop(columns = list(set(pd_timeslots.columns) - {'dateSlot', 'timeFrom', 'timeTo', 'restCount'}), inplace=True)

    # Subset timeslots on not yet emailed timeslots
    pd_emailed = None
    if os.path.exists('data//emailed.xlsx'):
        pd_emailed = pd.read_excel('data//emailed.xlsx')
        pd_timeslots = pd_timeslots.merge(pd_emailed, on=['timeFrom', 'timeTo', 'dateSlot'], indicator=True, how='left')
        l_drop = pd_timeslots[pd_timeslots['_merge'].isin(['both', 'right_only'])].index
        pd_timeslots.drop(l_drop, inplace=True)
   
    if len(pd_timeslots) > 0:

        html_table = pretty_html_table.build_table(pd_timeslots[['dateSlot', 'timeFrom', 'timeTo']], 'blue_light')

        b_send = send_mail.sendmail(
            l_to=[
                'martienstam@gmail.com',
                'pieter.stam85@gmail.com'
                ],
            s_header='Beschikbare tickets Vechtsebanen:\n\n',
            s_body=html_table,
            s_footer='\n\ngroeten,\n\n\n Martien Stam',
            s_subject='Vechtsebanen scrape'
            )

        # Store results for next run        
        pd.concat([pd_emailed, pd_timeslots])[['dateSlot', 'timeFrom', 'timeTo']].to_excel('data//emailed.xlsx', index=False)


if __name__ == '__main__':
    main()
