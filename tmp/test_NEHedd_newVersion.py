jobs = [
    {'id': 'j1', 'm1_time': 10, 'm2_time': 5, 'due_date': 10},
    {'id': 'j2', 'm1_time': 6, 'm2_time': 7, 'due_date': 5},
    {'id': 'j3', 'm1_time': 8, 'm2_time': 4, 'due_date': 20},
    {'id': 'j4', 'm1_time': 9, 'm2_time': 6, 'due_date': 10},
    {'id': 'j5', 'm1_time': 3, 'm2_time': 11, 'due_date': 5}
]




# Αριθμός εργοστασίων
F = 2

def NEHDedd(jobs, F):
    # Ταξινόμηση εργασιών βάσει ημερομηνίας λήξης σε αύξουσα σειρά
    jobs_sorted = sorted(jobs, key=lambda x: x['due_date'])


    print(jobs_sorted)
    
    # Αρχικοποίηση εργοστασίων
    factories = [[] for _ in range(F)]

    # Συνάρτηση υπολογισμού συνολικής καθυστέρησης και χρόνου εκτέλεσης
    def compute_total_tardiness(factory):
        total_tardiness = 0
        current_time_m1 = 0
        current_time_m2 = 0
        for job in factory:
            start_time_m1 = current_time_m1
            current_time_m1 += job['m1_time']
            start_time_m2 = max(current_time_m1, current_time_m2)
            current_time_m2 = start_time_m2 + job['m2_time']
            tardiness = max(0, current_time_m2 - job['due_date'])
            total_tardiness += tardiness
            job['start_time_m1'] = start_time_m1
            job['end_time_m1'] = current_time_m1
            job['start_time_m2'] = start_time_m2
            job['end_time_m2'] = current_time_m2
        return total_tardiness

    # Εισαγωγή εργασιών
    for job in jobs_sorted:
        min_tardiness = float('inf')
        best_factory_index = -1
        best_position = -1

        # Δοκιμή σε όλες τις θέσεις όλων των εργοστασίων
        for f in range(F):
            for position in range(len(factories[f]) + 1):
                # Δοκιμή τοποθέτησης της εργασίας στην τρέχουσα θέση
                temp_factory = factories[f][:position] + [job] + factories[f][position:]
                tardiness = compute_total_tardiness(temp_factory)
                
                # Εύρεση της θέσης με τη μικρότερη καθυστέρηση
                if tardiness < min_tardiness:
                    min_tardiness = tardiness
                    best_factory_index = f
                    best_position = position

        # Εισαγωγή της εργασίας στη βέλτιστη θέση του κατάλληλου εργοστασίου
        factories[best_factory_index].insert(best_position, job)

    return factories

# Εκτέλεση του αλγορίθμου NEHDedd
optimal_factories_schedule = NEHDedd(jobs, F)
optimal_factories_schedule_result = [
    {
        "Factory": i + 1,
        "Schedule": [
            {
                "Job ID": job['id'],
                "Due Date": job['due_date'],
                "M1 Time": job['m1_time'],
                "M2 Time": job['m2_time'],
                "Start Time M1": job['start_time_m1'],
                "End Time M1": job['end_time_m1'],
                "Start Time M2": job['start_time_m2'],
                "End Time M2": job['end_time_m2']
            } for job in factory
        ]
    } for i, factory in enumerate(optimal_factories_schedule)
]
NEHDedd(jobs, F)


print("-----------------------------------------")
print(optimal_factories_schedule_result)


