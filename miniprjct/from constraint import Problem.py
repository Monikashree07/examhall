from constraint import Problem

def exam_seating_allocation(num_students, num_rooms, room_capacities, student_preferences):
    problem = Problem()

    # Define variables (seats) and their domains
    for student in range(num_students):
        for room in range(num_rooms):
            problem.addVariable((student, room), range(room_capacities[room]))

    # Add constraints
    for student in range(num_students):
        problem.addConstraint(lambda *seats: len(set(seats)) == len(seats), [(student, room) for room in range(num_rooms)])
        for pref_student in student_preferences[student]:
            problem.addConstraint(lambda seat1, seat2: abs(seat1 - seat2) > 1, [(student, room1), (pref_student, room2)])

    # Solve the problem
    solutions = problem.getSolutions()
    
    return solutions

# Example usage
num_students = 4
num_rooms = 2
room_capacities = [10, 10]  # Capacities of each room
student_preferences = {
    0: [1, 2],  # Student 0 prefers to sit at least 2 seats away from students 1 and 2
    1: [0, 2],
    2: [0, 1],
    3: []  # Student 3 has no preferences
}

solutions = exam_seating_allocation(num_students, num_rooms, room_capacities, student_preferences)
print("Number of solutions:", len(solutions))
for solution in solutions:
    print(solution)
