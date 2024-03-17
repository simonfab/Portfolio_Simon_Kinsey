''' Initial capstone project for Hyperion course
    Some simple functions and calculations around interest and repayments

    NB I have left the pseudo code in at the end
'''

# Import libraries
import math

# Define functions

def print_messages(message):
    '''main print engine - prints supplied message'''
    print(message)

def validate_integers (user_entry):
    '''validate_integers - standard function to recieve input,
       try to convert to integer and that its greater than 0
       returns integer - otherwise returns none'''
    try:
        user_entry = int(user_entry)
        if user_entry > 0:
            return user_entry
        else:
            print ("Value must be greater than 0")
            return None
    except ValueError:
        print_messages ("Invalid input - please enter a number >0")

def validate_floats (user_entry):
    '''validate_floats - standard function to recieve input, 
       try to convert to float and entry is greater than 0
       returns float - otherwise returns none'''
    try:
        user_entry = float(user_entry)
        if user_entry > 0:
            return user_entry
        else:
            print ("Value must be greater than 0.0")
            return None
    except ValueError:
        print_messages ("Invalid input - please enter a number >0")

def bond_calculation (p,im,n):
    '''bond_calculation - p = pv of house; im = monthly interest rate and n = no of months
       returns monthly repayment'''
    repayment = round((im*p)/(1-(1+im)**(-n)),2)
    return repayment

def investment_calculation (p,r,t):
    '''investment interest calucator - p = initial deposit,
       r = annual rate of interest, t= number of years
       returns simple and compound interest and total interest earned'''
    # simple
    tot_amt_simp_c = round(p*(1+r*t),0)
    tot_int_simp_c = tot_amt_simp_c-p
    # compound
    tot_amt_comp_c = round(p*math.pow((1+r),t),0)
    tot_int_comp_c = tot_amt_comp_c-p
    return tot_amt_simp_c, tot_int_simp_c, tot_amt_comp_c, tot_int_comp_c

# main code loop follows

print ("\nWelcome to the finance calculators.\n")

while True:
    # lets get user selection, relevant inputs and process:

    init_choice = input("You can choose from:\n" + "\"Investment\""
                        + " - to calculate the total amount you may earn on your investment\n"
                        + "\"Bond\" - to calculate how much it will "
                        + "cost to pay off your mortgage or\n"
                        + "\"Quit\" - to terminate program\n\n"
                        + "Please enter your selection...\n")

    # process the initial choice to get consistent shortened string
    # - this could be just 1 char given diff words
    final_choice = init_choice.replace(" ","").lower()[0:4]

    # if user wants to quit use full "quit" or short cut q
    if final_choice == "quit" or init_choice =="q":
        #carry_on = False
        break

    # deal with investment
    elif final_choice =="inve" or init_choice =="i":
        print("We're going to see how much you can earn by saving a lump sum...\n\n")
        print("we just need answers to a couple of easy quesions:\n")

        while True:
            # get initial deposit...in hindsight this could have
            # been done with the house value etc in a single routine
            initial_deposit_input = input("Enter the amount you want to deposit...")
            initial_deposit = validate_integers (initial_deposit_input)
            if initial_deposit is not None:
                print (f"Your initial deposit is £{initial_deposit:,.0f}")
                break
        while True:
            # get interest rate to 4dps
            int_rate_input = input("Enter the expected interest rates...")
            curr_int_rate = validate_floats (int_rate_input)
            if curr_int_rate is not None:
                curr_int_rate = round(curr_int_rate/100,4)
                print (f"Your current interest rate is {curr_int_rate*100:,.2f}%")
                break
        while True:
            # get number of years to save
            No_of_years_input = input("Enter the expected number of YEARS to save...")
            No_of_years = validate_floats (No_of_years_input)
            if No_of_years is not None:
                No_of_years = round(No_of_years,2)
                print (f"Your expected saving period is {No_of_years} years")
                break

        print (f"\nIn summary:\nAmount to deposit - £{initial_deposit:,.0f}\n"
              f"Interest rate - {curr_int_rate*100:,.2f}% pa\n"
              f"Period to save - {No_of_years} years\n")

        # call the calculations
        (total_simp_ret, total_simp_int,
        total_cum_ret, total_cum_int) = \
        investment_calculation(initial_deposit, curr_int_rate, No_of_years)

        # ask the user what result they would like to see
        while True:
            user_int_choice = input("You can choose to see the results "
                                    + "on two different calucations - choose from:\n"
                                    + "\"Simple\" - to see the total amount "
                                    + "returned from simple interest calculation or\n"
                                    + "\"Compound\" - to how much you would earn "
                                    + "with compound intereest...\n"
                                    + "\"Move on\" to do some more calculations...\n")

            #process the initial choice to get consistent shortened string:
            user_int_choice_final = user_int_choice.replace(" ","").lower()[0:4]

            # show simple results (s is the short cut)
            if user_int_choice_final == "simp" or user_int_choice =="s":
                print (f"The simple amount returned after {No_of_years:,.2f} "
                       f"years will be £{total_simp_ret:,.0f}\n"
                       f"The simple interest earned would be £{total_simp_int:,.0f}\n")
            elif user_int_choice_final == "comp" or user_int_choice =="c":
                print (f"The compound amount returned after {No_of_years:,.2f} "
                       f"years will be £{total_cum_ret:,.0f}\n"
                       f"The compound interest earned would be £{total_cum_int:,.0f}\n")
            else:
                break

  # Deal with bond calculation
    # deal with mortgage repayment (short cut is 'b')
    elif final_choice == "bond" or init_choice =="b":
        print("We're going to see how much to repay your house off...\n\n")
        print("We just need answers to a couple of easy quesions:\n")

        while True:
            #get value of house - really this is the amount of money needed to pay for the house...
            curr_house_value_input = input("Enter the value of the house...")
            curr_house_value = validate_integers (curr_house_value_input)
            if curr_house_value is not None:
                print (f"Your house value is approx £{curr_house_value:,.0f}")
                break
        while True:
            #get interest rate
            int_rate_input = input("Enter the expected interest rate...")
            curr_int_rate = validate_floats (int_rate_input)
            if curr_int_rate is not None:
                monthly_int_rate = round(curr_int_rate/100/12,4)
                curr_int_rate_extra = curr_int_rate+1
                monthly_int_rate_extra = round(curr_int_rate_extra/100/12,4)
                print (f"Your current annual interest rate is {curr_int_rate}% ")
                break
        while True:
            #get number of months to repay
            No_of_months_input = input("Enter the expected number of MONTHS to repay...")
            No_of_months = validate_integers (No_of_months_input)
            if No_of_months is not None:
                print (f"Your expected repayment period is {No_of_months} or "
                       f"{round(No_of_months/12,2)} years")
                break
        print (f"\nIn summary:\nAmount to pay - £{curr_house_value:,.0f}\n"
              f"Interest rate - {curr_int_rate}% pa\n"
              f"Period to pay - {No_of_months} months\n")

        # let show the results
        # first get the info from the function bond_calculation
        bond_repyament = bond_calculation(curr_house_value, monthly_int_rate,No_of_months)
        total_paid = bond_repyament*No_of_months
        total_int_paid = total_paid-curr_house_value

        # tell the user
        print (f"The amount of the monthly bond is £{bond_repyament:,.2f}\n"
              f"The total amount payable is £{total_paid:,.2f}\n"
              f"Total interest payable is £{total_int_paid:,.2f}\n")

        # see if the user wants to know what happens if interest rates go up by a point?
        show_comparison = input("Would you like to see what would happen if interest rates "
                                "increased by 1%? - just enter \"y\" or \"n\"...")

        # if show comparison required
        if show_comparison == "y":
            bond_repyament_extra =\
            bond_calculation(curr_house_value,monthly_int_rate_extra,No_of_months)
            total_paid_hr = bond_repyament_extra * No_of_months
            total_int_paid_hr = total_paid_hr-curr_house_value
            print (f"\nIf interest rates increased by just 1% to "
                  f"{curr_int_rate_extra}%:\n"
                  f"The amount of the increased monthly bond would be "
                  f"£{bond_repyament_extra:,.2f}\n"
                  f"The monthly extra payable would be "
                  f"£{bond_repyament_extra - bond_repyament:,.2f}\n"
                  f"Total extra interest payable would be "
                  f"£{total_int_paid_hr - total_int_paid:,.2f}\n\n")

# get ready to do it again
        print ("Would you like to do another calculation...")

# inital string result nonsensical
    else:
        print ("You have entered nonsense! (an unrecognised string) "
                "- please try again or quit...\n\n")

# The following executes on quitting/break
print_messages ("Thanks for using the system")  # This prints 'False' when 'quit is entered
