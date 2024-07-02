from main . models import YearClassTerm

class YearClassTermViews:

    def add_year_class_term(self, request, current_employee, 
                                 new_student, classID, new_year_class, streamID, termID, student_typeID,
                                 current_fees, current_year):

           #add student to class_year_term
           new_year_class_term = YearClassTerm()
           new_year_class_term.campusID = current_employee.campusID
           new_year_class_term.businessID = current_employee.businessID
           new_year_class_term.categoryID = classID.categoryID
           new_year_class_term.classID = classID
           new_year_class_term.levelID = classID.levelID
           new_year_class_term.streamID = streamID
           new_year_class_term.student_typeID = student_typeID
           new_year_class_term.studentID = new_student
           new_year_class_term.year_classID= new_year_class
           new_year_class_term.year = current_year
           new_year_class_term.class_name = classID.class_name
           new_year_class_term.term_name  = termID.term_name
           new_year_class_term.stream_name  = streamID.stream_name
           new_year_class_term.student_name = new_student.fullname
           new_year_class_term.fees = float(current_fees.amount_required)
           new_year_class_term.balance = float(current_fees.amount_required)
           new_year_class_term.save()

           return new_year_class_term
