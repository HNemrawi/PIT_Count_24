# Column mappings and filtering
NE_mapping = {
    'Timestamp': 'Timestamp',
    #adult_1
    'Gender': 'Gender',
    'Race/Ethnicity': 'Race/Ethnicity',
    'Age Range': 'age_range',
    'Currently Fleeing Domestic/Sexual/Dating Violence': 'DV',
    'Veteran Status': 'vet',
    '**SURVEYOR: Does this person have a disabling condition?': 'disability',
    'How long have you been literally homeless?': 'homeless_long',
    'How long have you been literally homeless this time?': 'homeless_long_this_time',
    'Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?': 'homeless_times',
    'In total, how long did you stay in shelters or on the streets for those times?' : 'homeless_total',
    'Is this the first time you have stayed in a place not meant for human habitation, in an emergency shelter, in a motel/hotel room paid for by an organization, or transitional housing?': 'first_time',
    'Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'chronic_condition',
    'Specific length of time literally homeless:' : 'specific_homeless_long',
    'Specific length of time literally homeless this time' : 'specific_homeless_long_this_time',
    #household
    # 'Is/was anyone in your household staying with you tonight/last night (Wednesday night)?': 'has_company',
    # 'Which of the following describes the household that is/was with you on Wednesday night?': 'household',
    #adult_2
    'Adult/Parent #2: Gender': 'adult_2_Gender',
    'Adult/Parent #2: Race/Ethnicity': 'adult_2_Race/Ethnicity',
    'Adult/Parent #2: Age Range': 'adult_2_age_range',
    'Adult/Parent #2: Currently Fleeing Domestic/Sexual/Dating Violence': 'adult_2_DV',
    'Adult/Parent #2: Veteran Status': 'adult_2_vet',
    '**SURVEYOR: Does Adult/Parent #2 have a disabling condition?' : 'adult_2_disability',
    'Adult/Parent #2: How long have you been literally homeless?' : 'adult_2_homeless_long',
    'Adult/Parent #2: How long have you been literally homeless this time?': 'adult_2_homeless_long_this_time',
    'Adult/Parent #2: Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?': 'adult_2_homeless_times',
    'Adult/Parent #2: In total, how long did you stay in shelters or on the streets for those times?' : 'adult_2_homeless_total',
    'Adult/Parent #2: Is this the first time you have stayed in a place not meant for human habitation, in an emergency shelter, in a motel/hotel room paid for by an organization, or transitional housing?' : 'adult_2_first_time',
    'Adult/Parent #2: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'adult_2_chronic_condition',
     #adult_3
    'Adult/Parent #3: Gender': 'adult_3_Gender',
    'Adult/Parent #3: Race/Ethnicity': 'adult_3_Race/Ethnicity',
    'Adult/Parent #3: Age Range': 'adult_3_age_range',
    'Adult/Parent #3: Currently Fleeing Domestic/Sexual/Dating Violence': 'adult_3_DV',
    'Adult/Parent #3: Veteran Status': 'adult_3_vet',
    '**SURVEYOR: Does Adult/Parent #2 have a disabling condition?' : 'adult_3_disability',
    'Adult/Parent #3: How long have you been literally homeless?' : 'adult_3_homeless_long',
    'Adult/Parent #3: How long have you been literally homeless this time?': 'adult_3_homeless_long_this_time',
    'Adult/Parent #3: Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?': 'adult_3_homeless_times',
    'Adult/Parent #3: In total, how long did you stay in shelters or on the streets for those times?' : 'adult_3_homeless_total',
    'Adult/Parent #3: Is this the first time you have stayed in a place not meant for human habitation, in an emergency shelter, in a motel/hotel room paid for by an organization, or transitional housing?' : 'adult_3_first_time',
    'Adult/Parent #3: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'adult_3_chronic_condition',
    #children
    'Do you need to add information for a child in the household?': 'child_1',
    'Child #1: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_1_chronic_condition',
    'Child #1: Gender': 'child_1_Gender',
    'Child #1: Race/Ethnicity': 'child_1_Race/Ethnicity',
    
    'Do you need to add information for another child?': 'child_2',
    'Child #2: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_2_chronic_condition',
    'Child #2: Gender': 'child_2_Gender',
    'Child #2: Race/Ethnicity': 'child_2_Race/Ethnicity',
    
    'Do you need to add information for a third child?': 'child_3',
    'Child #3: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_3_chronic_condition',
    'Child #3: Gender': 'child_3_Gender',
    'Child #3: Race/Ethnicity': 'child_3_Race/Ethnicity',
    
    'Do you need to add information for a fourth child?': 'child_4',
    'Child #4: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_4_chronic_condition',
    'Child #4: Gender': 'child_4_Gender',
    'Child #4: Race/Ethnicity': 'child_4_Race/Ethnicity',
    
    'Do you need to add information for a fifth child?': 'child_5',
    'Child #5: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_5_chronic_condition',
    'Child #5: Gender': 'child_5_Gender',
    'Child #5: Race/Ethnicity': 'child_5_Race/Ethnicity',
    
    'Do you need to add information for a sixth child?': 'child_6',
    'Child #6: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_6_chronic_condition',
    'Child #6: Gender': 'child_6_Gender',
    'Child #6: Race/Ethnicity': 'child_6_Race/Ethnicity'}

WI_mapping = {
    'Timestamp': 'Timestamp',
    #adult_1
    'Gender': 'Gender',
    'Race/Ethnicity': 'Race/Ethnicity',
    'Age Range': 'age_range',
    'Are you a victim/survivor of domestic violence?': 'DV',
    'Have you ever served on active duty in the Armed Forces of the United States?': 'vet',
    '**SURVEYOR: Does this person have a disabling condition?': 'disability',
    'How long have you been homeless?': 'homeless_long',
    'How long have you been homeless this time?': 'homeless_long_this_time',
    'Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?': 'homeless_times',
    'In total, how long did you stay in shelters or on the streets for those times?' : 'homeless_total',
    "Is this the first time you've been homeless?": 'first_time',
    'Do you have, or have you ever been diagnosed with, any of the following?' : 'chronic_condition',
    'Specific length of time homeless' : 'specific_homeless_long',
    'Specific length of time homeless this time' : 'specific_homeless_long_this_time',
    #household
    # 'Is (was) anyone from your current family household staying with you tonight (on Wednesday night)?': 'has_company',
    # 'Which of the following describes the family household that is/was with you on Wednesday night?': 'household',
    #adult_2
    'Adult/Parent #2: Gender': 'adult_2_Gender',
    'Adult/Parent #2: Race/Ethnicity': 'adult_2_Race/Ethnicity',
    'Adult/Parent #2: Age Range': 'adult_2_age_range',
    'Adult/Parent #2: Are you a victim/survivor of domestic violence?': 'adult_2_DV',
    'Adult/Parent #2: Have you ever served on active duty in the Armed Forces of the United States?': 'adult_2_vet',
    '**SURVEYOR: Does Adult/Parent #2 have a disabling condition?' : 'adult_2_disability',
    'Adult/Parent #2: How long have you been homeless?' : 'adult_2_homeless_long',
    'Adult/Parent #2: How long have you been homeless this time?': 'adult_2_homeless_long_this_time',
    'Adult/Parent #2: Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?': 'adult_2_homeless_times',
    'Adult/Parent #2: In total, how long did you stay in shelters or on the streets for those times?' : 'adult_2_homeless_total',
    "Adult/Parent #2: Is this the first time you've been homeless?" : 'adult_2_first_time',
    'Adult/Parent #2: Do you have, or have you ever been diagnosed with, any of the following?' : 'adult_2_chronic_condition',
    
    #children
    'Do you need to add information for a child in the household?': 'child_1',
    'Child #1: Gender': 'child_1_Gender',
    'Child #1: Race/Ethnicity': 'child_1_Race/Ethnicity',
    
    'Do you need to add information for another child?': 'child_2',
    'Child #2: Gender': 'child_2_Gender',
    'Child #2: Race/Ethnicity': 'child_2_Race/Ethnicity',
    
    'Do you need to add information for a third child?': 'child_3',
    'Child #3: Gender': 'child_3_Gender',
    'Child #3: Race/Ethnicity': 'child_3_Race/Ethnicity',
    
    'Do you need to add information for a fourth child?': 'child_4',
    'Child #4: Gender': 'child_4_Gender',
    'Child #4: Race/Ethnicity': 'child_4_Race/Ethnicity',
    
    'Do you need to add information for a fifth child?': 'child_5',
    'Child #5: Gender': 'child_5_Gender',
    'Child #5: Race/Ethnicity': 'child_5_Race/Ethnicity',
    
    'Do you need to add information for a sixth child?': 'child_6',
    'Child #6: Gender': 'child_6_Gender',
    'Child #6: Race/Ethnicity': 'child_6_Race/Ethnicity'}

condition_mapping = {
    'Physical disability': 'Physical Condition',
    'Psychiatric or emotional conditions such as depression or schizophrenia': 'Mental Health',
    'PTSD (Post Traumatic Stress Disorder)': 'Mental Health',
    'Mental Health': 'Mental Health',
    'Substance Use Disorder (Alcohol, Drugs, or Both)': 'Substance Use Disorder (Alcohol, Drugs, or Both)',
    'AIDS or HIV-related illness': 'HIV/AIDS',
    'Ongoing health problems or medical conditions such as diabetes, cancer, o': 'Other Chronic Health Condition',
    'Traumatic brain or head injury': 'Other Chronic Health Condition',
    "Don't Know/Refused": "Don't Know/Refused",
    'None of the above': 'None of the above'
}

age_ranges = ['25-34', '35-44', '45-54', '55-64', '65+']

gender_categories = {
    'Woman (Girl if child)': 'Woman_Girl',
    'Man (Boy if child)': 'Man_Boy',
    'Culturally Specific Identity': 'Culturally_Specific_Identity',
    'Transgender': 'Transgender',
    'Non-Binary': 'Non_Binary',
    'Questioning': 'Questioning',
    'Different Identity': 'Different_Identity',
    'More Than One Gender': 'More_Than_One_Gender'
}

race_categories = {
    'Indigenous (American Indian/Alaska Native/Indigenous)': 'Indigenous',
    'Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o': 'Indigenous_Hispanic',
    'Asian/Asian American': 'Asian',
    'Asian/Asian American & Hispanic/Latina/e/o': 'Asian_Hispanic',
    'Black/African American/African': 'Black',
    'Black/African American/African & Hispanic/Latina/e/o': 'Black_Hispanic',
    'Hispanic/Latina/e/o': 'Hispanic',
    'Middle Eastern/North African': 'Middle_Eastern_North_African',
    'Middle Eastern/North African & Hispanic/Latina/e/o': 'Middle_Eastern_North_African_Hispanic',
    'Native Hawaiian/Pacific Islander': 'Native_Hawaiian',
    'Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o': 'Native_Hawaiian_Hispanic',
    'White': 'White',
    'White & Hispanic/Latina/e/o': 'White_Hispanic',
    'Multi-Racial & Hispanic/Latina/e/o': 'Multi_Racial_Hispanic',
    'Multi-Racial (not Hispanic/Latina/e/o)': 'Multi_Racial_Non_Hispanic'
}

condition_categories = {
    'Mental Health': 'Serious_Mental_Illness',
    'Substance Use Disorder (Alcohol, Drugs, or Both)': 'Substance_Use_Disorder',
    'Physical Condition': 'Physical_Condition',
    'HIV/AIDS': 'HIV_AIDS',
    'Developmental Condition': 'Developmental_Condition',
    'Other Chronic Health Condition': 'other_Condition'
}

household_categories = {
    'Household with Children': 'Households_with_Child',
    'Household without Children': 'Households_without_Children',
    'Household with Only Children': 'Households_with_Only_Children'
}