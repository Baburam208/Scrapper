from datetime import date, timedelta

def return_dates(start_date, end_date):    #Compute the dates
    dates_list= []
    delta = end_date - start_date
       
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        dates_list.append(str(day))
    return dates_list
