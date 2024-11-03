import random
import matplotlib.pyplot as plt
student_dict = {}

with open('records.csv','r') as file:
    headers = file.readline()

    for line in file:
        line = line.split(',')
        tutorial_group = line[0]
        student_id = line[1]

        if tutorial_group not in student_dict:
            student_dict[tutorial_group] = {}

        student_dict[tutorial_group][student_id] = {
            'School': line[2],
            'Name': line[3],
            'Gender': line[4],
            'CGPA': float(line[5].strip()),
        }

def count_student_by_school(student):
    schools = {}
    for student_id, student_data in student.items():
        school = student_data['School']
        if school not in schools:
            schools[school] = []
        schools[school].append(student_id)
    return schools

def classify_cgpa(cgpa):
    if cgpa >= 4.5:
        return 'High'
    elif 4.0 <= cgpa < 4.5:
        return 'Medium'
    else:
        return 'Low'

def pick_student(students, cgpa_range, student):
    candidates = [student_id for student_id in students if classify_cgpa(student[student_id]['CGPA']) == cgpa_range]
    if candidates:
        return random.choice(candidates)
    return random.choice(students)

def find_most_populated_school(schools):
    max_students = 0
    for school, students in schools.items():
        if len(students) > max_students:
            max_students = len(students)
            most_populated_school = school
    return most_populated_school

def form_group(student):
    schools = count_student_by_school(student)
    groups = []
    
    while True:
        group = []

        if not schools:
            break
        
        most_populated_school = find_most_populated_school(schools)
        first_student_id = random.choice(schools[most_populated_school])
        group.append(first_student_id)
        
        schools[most_populated_school].remove(first_student_id)
        if len(schools[most_populated_school]) == 0:
            del schools[most_populated_school]

        first_student_cgpa = student[first_student_id]['CGPA']
        first_student_cgpa_range = classify_cgpa(first_student_cgpa)
        
        for i in range(4):
            remaining_schools = list(schools.keys())
            next_school = random.choice(remaining_schools)
            if first_student_cgpa_range == 'High':
                next_student_id = pick_student(schools[next_school], 'Medium', student) or pick_student(schools[next_school], 'Low', student)
            elif first_student_cgpa_range == 'Low':
                next_student_id = pick_student(schools[next_school], 'Medium', student) or pick_student(schools[next_school], 'High', student)
            else:
                next_student_id = random.choice(schools[next_school])
                
            group.append(next_student_id)
            schools[next_school].remove(next_student_id)
            if len(schools[next_school]) == 0:
                del schools[next_school]

        if len(group) >= 5:
            groups.append(group)
    
    return groups

def calc_cgpa(group_dict):
    average = []
    minimum = []
    maximum = []

    for tutorial_group, groups in group_dict.items():
        for group in groups:
            total_cgpa = sum(student_dict[tutorial_group][student_id]['CGPA'] for student_id in group)
            number = len(group)
            
            if number > 0:
                average_cgpa = total_cgpa/number
                min_cgpa = min(student_dict[tutorial_group][student_id]['CGPA'] for student_id in group)
                max_cgpa = max(student_dict[tutorial_group][student_id]['CGPA'] for student_id in group)

            average.append(average_cgpa)
            minimum.append(min_cgpa)
            maximum.append(max_cgpa)

    return average, minimum, maximum

def calc_gender(group_dict):
    pass

def calc_school(group_dict):
    total_different_schools = 0
    total_groups = 0
#   Iterate through each tutorial group    
    for tutorial_group, groups in group_dict.items():
#   Iterate through each team in the current tutorial group
        for group in groups:
#   Use set to remove duplicate schools in the current group
#   Retrieve the school of each student in the group
            schools_in_group = set(student_dict[tutorial_group][student_id]['School'] for student_id in group)
#   Add the number of unique schools in the current group to the total count
            total_different_schools += len(schools_in_group)
#   Increase the counter value by 1
            total_groups += 1
#   Calculate the average number of different schools per group
    if total_groups > 0:
        return total_different_schools / total_groups
    else:
        return 0

def export(group_dict,filename='grouped_students.csv'):
    with open(filename, 'w') as file:  #opens file in write mode 
        file.write("Tutorial Group,Team Assigned ,Student ID,School,Name,Gender,CGPA\n") ## writes header in file
        for tutorial_group, groups in group_dict.items(): # for each group in in file
            group_number = 1
            for group in groups: #for each team in teams, put in the value
                for student_id in group:
                    student = student_dict[tutorial_group][student_id] 
                    file.write(
                        f"{tutorial_group},Team{group_number},{student_id},"
                        f"{student['School']},{student['Name']},{student['Gender']},{student['CGPA']}\n"
                    )
                group_number += 1

all_groups = {}
for tutorial_group, student in student_dict.items():
    all_groups[tutorial_group] = form_group(student)

#data = calc_cgpa(all_groups)
#plt.hist(data[0])
#plt.hist(data[1])
#plt.hist(data[2])
#plt.show()

# overall data for gender, school, and CGPA distributions
gender_counts = {'Male': 0, 'Female': 0}
school_counts = {}
cgpa_categories = {'High': 0, 'Medium': 0, 'Low': 0}

for tutorial_group, groups in all_groups.items():
    for group in groups:
        for student_id in group:
            student = student_dict[tutorial_group][student_id]
            
            # Gender count
            gender_counts[student['Gender']] += 1
            
            # School count
            school = student['School']
            if school not in school_counts:
                school_counts[school] = 0
            school_counts[school] += 1
            
            # CGPA category count
            cgpa_category = classify_cgpa(student['CGPA'])
            cgpa_categories[cgpa_category] += 1

#  Gender Distribution
plt.figure(figsize=(10, 4))
plt.bar(gender_counts.keys(), gender_counts.values(), color=['blue', 'pink'])
plt.title("Gender Distribution")
plt.ylabel("Count")
plt.show()

# School Distribution
plt.figure(figsize=(10, 4))
plt.bar(school_counts.keys(), school_counts.values(), color='skyblue')
plt.title("School Distribution")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.show()

# CGPA Distribution
plt.figure(figsize=(10, 4))
plt.bar(cgpa_categories.keys(), cgpa_categories.values(), color=['green', 'orange', 'red'])
plt.title("CGPA Distribution")
plt.ylabel("Count")
plt.show()

#Export all groups to CSV
#export(all_groups)
