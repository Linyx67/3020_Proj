from django.db import models
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from hris_app.models import StaffUser, CustomUser, AdminUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from .utility import code_format
from admin_app.managers import EmployeeManager, LeaveManager
# Create your models here.


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    stafff_id = models.ForeignKey(StaffUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReport(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(StaffUser, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Religion(models.Model):
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125, null=True, blank=True)

    created = models.DateTimeField(
        verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Religion')
        verbose_name_plural = _('Religions')
        ordering = ['name', 'created']

    def __str__(self):
        return self.name


class Emergency(models.Model):
    FATHER = 'Father'
    MOTHER = 'Mother'
    SIS = 'Sister'
    BRO = 'Brother'
    UNCLE = 'Uncle'
    AUNTY = 'Aunty'
    HUSBAND = 'Husband'
    WIFE = 'Wife'
    FIANCE = 'Fiance'
    FIANCEE = 'Fiancee'
    COUSIN = 'Cousin'
    NIECE = 'Niece'
    NEPHEW = 'Nephew'
    SON = 'Son'
    DAUGHTER = 'Daughter'

    EMERGENCY_RELATIONSHIP = (
        (FATHER, 'Father'),
        (MOTHER, 'Mother'),
        (SIS, 'Sister'),
        (BRO, 'Brother'),
        (UNCLE, 'Uncle'),
        (AUNTY, 'Aunty'),
        (HUSBAND, 'Husband'),
        (WIFE, 'Wife'),
        (FIANCE, 'Fiance'),
        (COUSIN, 'Cousin'),
        (FIANCEE, 'Fiancee'),
        (NIECE, 'Niece'),
        (NEPHEW, 'Nephew'),
        (SON, 'Son'),
        (DAUGHTER, 'Daughter'),
    )

    # access table: employee.emergency_set.
    employee = models.ForeignKey(
        'Employee', on_delete=models.CASCADE, null=True, blank=True)
    fullname = models.CharField(
        _('Fullname'), help_text='who should we contact ?', max_length=255, null=True, blank=False)
    tel = PhoneNumberField(default='+233240000000', null=False, blank=False,
                           verbose_name='Phone Number (Example +233240000000)', help_text='Enter number with Country Code Eg. +233240000000')
    location = models.CharField(
        _('Place of Residence'), max_length=125, null=True, blank=False)
    relationship = models.CharField(_('Relationship with Person'), help_text='Who is this person to you ?',
                                    max_length=8, default=FATHER, choices=EMERGENCY_RELATIONSHIP, blank=False, null=True)

    created = models.DateTimeField(
        verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)

    class Meta:
        verbose_name = 'Emergency'
        verbose_name_plural = 'Emergency'
        ordering = ['-created']

    def __str__(self):
        return self.fullname

    created = models.DateTimeField(verbose_name=_(
        'Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(
        verbose_name=_('Updated'), auto_now=True, null=True)


class Employee(models.Model):

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    NOT_KNOWN = 'Not Known'

    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        (NOT_KNOWN, 'Not Known'),
    )

    MR = 'Mr'
    MRS = 'Mrs'
    MSS = 'Mss'
    DR = 'Dr'
    SIR = 'Sir'
    MADAM = 'Madam'

    TITLE = (
        (MR, 'Mr'),
        (MRS, 'Mrs'),
        (MSS, 'Mss'),
        (DR, 'Dr'),
        (SIR, 'Sir'),
        (MADAM, 'Madam'),
    )

    FULL_TIME = 'Full-Time'
    PART_TIME = 'Part-Time'
    CONTRACT = 'Contract'
    INTERN = 'Intern'

    EMPLOYEETYPE = (
        (FULL_TIME, 'Full-Time'),
        (PART_TIME, 'Part-Time'),
        (CONTRACT, 'Contract'),
        (INTERN, 'Intern'),
    )

    # PERSONAL DATA
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    title = models.CharField(_('Title'), max_length=10,
                             default=MR, choices=TITLE, blank=False, null=True)
    image = models.FileField(_('Profile Image'), upload_to='profiles', default='default.png', blank=True,
                             null=True, help_text='upload image size less than 2.0MB')  # work on path username-date/image
    firstname = models.CharField(
        _('Firstname'), max_length=125, null=False, blank=False)
    lastname = models.CharField(
        _('Lastname'), max_length=125, null=False, blank=False)
    othername = models.CharField(
        _('Othername (optional)'), max_length=125, null=True, blank=True)
    sex = models.CharField(_('Gender'), max_length=10,
                           default=MALE, choices=GENDER, blank=False)
    email = models.EmailField(
        _('Email'), max_length=255, default=None, blank=True, null=True)
    tel = PhoneNumberField(default='+233240000000', null=False, blank=False,
                           verbose_name='Phone Number (Example +233240000000)', help_text='Enter number with Country Code Eg. +233240000000')
    bio = models.CharField(_('Bio'), help_text='your biography,tell me something about yourself eg. i love working ...',
                           max_length=255, default='', null=True, blank=True)
    birthday = models.DateField(_('Birthday'), blank=False, null=False)
    religion = models.ForeignKey(Religion, verbose_name=_(
        'Religion'), on_delete=models.SET_NULL, null=True, default=None)
    ssnitnumber = models.CharField(
        _('SSNIT Number'), max_length=30, null=True, blank=True)
    tinnumber = models.CharField(
        _('TIN'), max_length=15, null=True, blank=True)

    is_blocked = models.BooleanField(
        _('Is Blocked'), help_text='button to toggle employee block and unblock', default=False)
    is_deleted = models.BooleanField(
        _('Is Deleted'), help_text='button to toggle employee deleted and undelete', default=False)

    created = models.DateTimeField(verbose_name=_(
        'Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(
        verbose_name=_('Updated'), auto_now=True, null=True)

    # PLUG MANAGERS
    objects = EmployeeManager()

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['-created']

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        fullname = ''
        firstname = self.firstname
        lastname = self.lastname
        othername = self.othername

        if (firstname and lastname) or othername is None:
            fullname = firstname + ' ' + lastname
            return fullname
        elif othername:
            fullname = firstname + ' ' + lastname + ' '+othername
            return fullname
        return

    @property
    def get_age(self):
        current_year = datetime.date.today().year
        dateofbirth_year = self.birthday.year
        if dateofbirth_year:
            return current_year - dateofbirth_year
        return

    @property
    def can_apply_leave(self):
        pass

    def save(self, *args, **kwargs):
        '''
        overriding the save method - for every instance that calls the save method 
        perform this action on its employee_id
        added : March, 03 2019 - 11:08 PM

        '''
        get_id = self.employeeid  # grab employee_id number from submitted form field
        data = code_format(get_id)
        # pass the new code to the employee_id as its orifinal or actual code
        self.employeeid = data
        super().save(*args, **kwargs)  # call the parent save method
        # print(self.employeeid)


# Leave Related
SICK = 'sick'
CASUAL = 'casual'
EMERGENCY = 'emergency'
STUDY = 'study'

LEAVE_TYPE = (
    (SICK, 'Sick Leave'),
    (CASUAL, 'Casual Leave'),
    (EMERGENCY, 'Emergency Leave'),
    (STUDY, 'Study Leave'),
)

DAYS = 30


class Leave(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    startdate = models.DateField(verbose_name=_(
        'Start Date'), help_text='leave start date is on ..', null=True, blank=False)
    enddate = models.DateField(verbose_name=_(
        'End Date'), help_text='coming back on ...', null=True, blank=False)
    leavetype = models.CharField(
        choices=LEAVE_TYPE, max_length=25, default=SICK, null=True, blank=False)
    reason = models.CharField(verbose_name=_('Reason for Leave'), max_length=255,
                              help_text='add additional information for leave', null=True, blank=True)
    defaultdays = models.PositiveIntegerField(verbose_name=_(
        'Leave days per year counter'), default=DAYS, null=True, blank=True)

    # hrcomments = models.ForeignKey('CommentLeave') #hide

    # pending,approved,rejected,cancelled
    status = models.CharField(max_length=12, default='pending')
    is_approved = models.BooleanField(default=False)  # hide

    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = LeaveManager()

    class Meta:
        verbose_name = _('Leave')
        verbose_name_plural = _('Leaves')
        ordering = ['-created']  # recent objects

    def __str__(self):
        return ('{0} - {1}'.format(self.leavetype, self.user))

    @property
    def pretty_leave(self):
        '''
        i don't like the __str__ of leave object - this is a pretty one :-)
        '''
        leave = self.leavetype
        user = self.user
        employee = user.employee_set.first().get_full_name
        return ('{0} - {1}'.format(employee, leave))

    @property
    def leave_days(self):
        days_count = ''
        startdate = self.startdate
        enddate = self.enddate
        if startdate > enddate:
            return
        dates = (enddate - startdate)
        return dates.days

    @property
    def leave_approved(self):
        return self.is_approved == True

    @property
    def approve_leave(self):
        if not self.is_approved:
            self.is_approved = True
            self.status = 'approved'
            self.save()

    @property
    def unapprove_leave(self):
        if self.is_approved:
            self.is_approved = False
            self.status = 'pending'
            self.save()

    @property
    def leaves_cancel(self):
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = 'cancelled'
            self.save()

    # def uncancel_leave(self):
    # 	if  self.is_approved or not self.is_approved:
    # 		self.is_approved = False
    # 		self.status = 'pending'
    # 		self.save()

    @property
    def reject_leave(self):
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = 'rejected'
            self.save()

    @property
    def is_rejected(self):
        return self.status == 'rejected'

    # def save(self,*args,**kwargs):
    # 	data = self.defaultdays
    # 	days_left = data - self.leave_days
    # 	self.defaultdays = days_left
    # 	super().save(*args,**kwargs)


# class Comment(models.Model):
# 	leave = models.ForeignKey(Leave,on_delete=models.CASCADE,null=True,blank=True)
# 	comment = models.CharField(max_length=255,null=True,blank=True)

# 	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
# 	created = models.DateTimeField(auto_now=False, auto_now_add=True)


# 	def __str__(self):
# 		return self.leave

class Publications(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)


class Awards(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
