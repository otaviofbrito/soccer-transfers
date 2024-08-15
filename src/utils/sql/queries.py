queries = {
    'get_all_clubs': "SELECT * FROM clubs",
    'get_all_not_loan_transfers': """ 
                                      SELECT * FROM transfers t WHERE transfer_type = 'Not loan'
                                      AND left_club_id NOT IN (-5, 75, 515)
                                      AND joined_club_id NOT IN (-5, 75, 515)
                                    """
}
