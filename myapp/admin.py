from django.contrib import admin
from .models import (
    Department, Student, Course, Enrollment, 
    Attendance, Grade, FeePayment
)


# ====================== DEPARTMENT ======================
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'description']
    search_fields = ['code', 'name']
    ordering = ['code']


# ====================== STUDENT ======================
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'full_name', 'department', 'status', 
                   'gender', 'email', 'phone', 'enrollment_date']
    list_filter = ['status', 'department', 'gender', 'enrollment_date']
    search_fields = ['student_id', 'first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['student_id', 'enrollment_date', 'created_at', 'updated_at']
    
    fieldsets = [
        ('Personal Information', {
            'fields': ('student_id', 'first_name', 'last_name', 'father_name', 
                      'mother_name', 'date_of_birth', 'gender', 'profile_pic')
        }),
        ('Contact Details', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Academic Details', {
            'fields': ('department', 'enrollment_date', 'status')
        }),
        ('System Info', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    ]

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'

    # Custom Actions
    actions = ['make_active', 'make_inactive', 'make_graduated']

    def make_active(self, request, queryset):
        queryset.update(status='active')
    make_active.short_description = "Mark selected students as Active"

    def make_inactive(self, request, queryset):
        queryset.update(status='inactive')
    make_inactive.short_description = "Mark selected students as Inactive"

    def make_graduated(self, request, queryset):
        queryset.update(status='graduated')
    make_graduated.short_description = "Mark selected students as Graduated"


# ====================== COURSE ======================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department', 'credits', 'is_active']
    list_filter = ['department', 'is_active', 'credits']
    search_fields = ['code', 'name', 'description']
    ordering = ['code']


# ====================== ENROLLMENT ======================
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrollment_date', 'status', 'grade']
    list_filter = ['status', 'enrollment_date', 'course__department']
    search_fields = ['student__student_id', 'student__first_name', 
                    'student__last_name', 'course__code', 'course__name']
    readonly_fields = ['enrollment_date']


# ====================== ATTENDANCE ======================
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'date', 'status', 'marked_by', 'marked_at']
    list_filter = ['status', 'date', 'course']
    search_fields = ['student__student_id', 'student__first_name', 'course__code']
    date_hierarchy = 'date'
    readonly_fields = ['marked_at']


# ====================== GRADE ======================
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'grade', 'total_marks', 
                   'obtained_marks', 'percentage', 'exam_date']
    list_filter = ['grade', 'exam_date', 'course__department']
    search_fields = ['student__student_id', 'course__code', 'course__name']
    readonly_fields = ['percentage']

    def percentage(self, obj):
        if obj.total_marks:
            return f"{(obj.obtained_marks / obj.total_marks * 100):.2f}%"
        return "-"
    percentage.short_description = 'Percentage'


# ====================== FEE PAYMENT ======================
@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'semester', 'amount', 'paid_amount', 
                   'remaining_amount_display', 'status', 'payment_date']
    list_filter = ['status', 'semester', 'payment_date']
    search_fields = ['student__student_id', 'student__first_name', 
                    'student__last_name', 'transaction_id']
    readonly_fields = ['remaining_amount_display', 'created_at']
    date_hierarchy = 'payment_date'

    def remaining_amount_display(self, obj):
        return obj.remaining_amount

    # Somewhere around line 120
    remaining_amount_display.short_description = 'Remaining Amount'

# Register your models here.
