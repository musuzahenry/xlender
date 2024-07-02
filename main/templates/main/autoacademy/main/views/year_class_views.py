from main . models import YearClass

class YearClassViews:

    def add_year_class(self, request, current_employee, new_student, classID, streamID, current_year):
           #adding student to new class year
           #=========================================================================
           new_year_class= YearClass()         
           new_year_class.campusID = current_employee.campusID
           new_year_class.businessID = current_employee.businessID
           new_year_class.categoryID = classID.categoryID
           new_year_class.classID = classID
           new_year_class.levelID = classID.levelID
           new_year_class.streamID = streamID
           new_year_class.studentID = new_student
           new_year_class.year = current_year
           new_year_class.class_name = classID.class_name
           new_year_class.stream_name  = streamID.stream_name
           #new_year_class.student_number = request.POST.get("school-student-number")
           new_year_class.student_name = new_student.fullname
           new_year_class.save()

           request.session["current_classID"] = new_year_class.id

           return new_year_class