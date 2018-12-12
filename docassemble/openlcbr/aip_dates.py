from datetime import timedelta
from docassemble.base.util import today

one_month = timedelta(days=30)
one_year = timedelta(days=365)
three_years = timedelta(days=(3*365))
ninety_days = timedelta(days=90)

events = []





def get_aip_dates(cohabitation, parties_have_child_by_birth_or_adoption, child_of_relationship_date, period_of_separation, declaration_of_irreconcilability, written_agreement):
    
    

    aip_start_dates = []
    aip_end_dates = []

    # Add events from the cohabitation
    events.append({'date': cohabitation.start_date, 'type': 'cohab_start', 'reconciliation': False})
    if cohabitation.has_terminated:
        events.append({'date': cohabitation.end_date, 'type': 'cohab_end', 'termination': True})

    # Save the first date on which there was a child of the relationship
    child = parties_have_child_by_birth_or_adoption
    if child: child_date = child_of_relationship_date

    # Add events for each of the periods of separation
    for pos in period_of_separation:
        events.append({'date': pos.start_date, 'type': 'cohab_end', 'termination': pos.intent})
        events.append({'date': pos.end_date, 'type': 'cohab_start', 'reconciliation': pos.reconciliation})

    # Add events for all the declarations of irreconcilability
    for doi in declaration_of_irreconcilability:
        aip_end_dates.append(doi.date)
    
    # Add events for all the written agreements
    for wa in written_agreement:
        aip_end_dates.append(wa.date)
    
    # PSUEDO    
    # Go through all the events
    for e in events:
        if is_cohab_start(e):
            # Birth, then cohabitation, one month from start.
            if child and is_after_birth_and_more_than_month_ago(e['date'], child_date):
                if not has_termination_within_one_month_after(e['date']):
                    aip_start_dates.append(e['date'] + one_month)
                    
            # Cohabitation, then birth in less than 35 months, one month from birth.
            elif child and is_within_35_months_of_birth(e['date'], child_date):

                # First, if the cohabitation lasted 3 years, it might be the start date.
                if is_more_than_three_years_ago(e['date']):
                    if not has_termination_within_three_years_after(e['date']):
                        aip_start_dates.append(e['date'] + three_years)

                # Second, if there was no termination within 1 month of the birth, the birth might be the start date.
                if is_more_than_one_month_ago(e['date']):
                    if not has_termination_within_one_month_after(child_date):
                        aip_start_dates.append(child_date + one_month)
            
            # No Birth before Or within 35 months of cohab start, three years from start.
            else:
                if is_more_than_three_years_ago(e['date']):
                    if not has_termination_within_three_years_after(e['date']):
                        aip_start_dates.append(e['date'] + three_years)
            

    # make the list of aip termination dates
    for e in events:
        if is_termination(e):
            if is_more_than_one_year_ago(e['date']):
                if not has_reconciliation_within_one_year_after(e['date']):
                    aip_end_dates.append(e['date'] + one_year)
    
    return earliest_unterminated_aip_start(aip_start_dates, aip_end_dates)
    
def earliest_unterminated_aip_start(aip_start_dates, aip_end_dates):
    found = None

    for s in aip_start_dates:
        terminated = False
        for e in aip_end_dates:
            if e > s:
                terminated = True
                break
        if found == None:
            found = s
        elif not terminated and s < found:
            found = s
    
    return s

def has_termination_within_ninety_days_after(date):
    for e in events:
        if e['date'] > date and e['date'] < date + ninety_days and is_termination(e):
            return True
    return False

def has_termination_within_one_month_after(date):
    for e in events:
        if e['date'] > date and e['date'] < date + one_month and is_termination(e):
            return True
    return False

def has_termination_within_three_years_after(date):
    for e in events:
        if e['date'] > date and e['date'] < date + three_years and is_termination(e):
            return True
    return False

def has_reconciliation_within_one_year_after(date):
    for e in events:
        if e['date'] > date and e['date'] < date + one_year and is_reconciliation(e):
            if not has_termination_within_ninety_days_after(e['date']):
                return True
    return False

def is_termination(e):
    if e['type'] == 'cohab_end' and e['termination']:
        return True
    else:
        return False

def is_reconciliation(e):
    if is_cohab_start(e) and e['reconciliation']:
        return True
    else:
        return False

def is_cohab_start(e):
    if e['type'] == 'cohab_start':
        return True
    else:
        return False

def is_after_birth_and_more_than_month_ago(date, birth_date):
    if date > birth_date and date < today() - one_month:
        return True
    else:
        return False

def is_within_35_months_of_birth(date, birth_date):
    if date < birth_date and date > birth_date - three_years + one_month:
        return True
    else:
        return False

def is_more_than_three_years_ago(date):
    if date < today() - three_years:
        return True
    else:
        return False

def is_more_than_one_year_ago(date):
    if date < today() - one_year:
        return True
    else:
        return False

def is_more_than_one_month_ago(date):
    if date < today() - one_month:
        return True
    else:
        return False