from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from hris_app.models import StaffUser, CustomUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _
from admin_app.managers import EmployeeManager, LeaveManager, PublicationManager
from .validate import max_value_current_year
# Create your models here.


# create requests module


class Requests(models.Model):
    STG = 'Study and Travel Grant'
    IVA = 'Institutional Visit Allowance'
    DTG = 'Development and Training Grant'
    BOOK = 'Book Grant'
    CLAIMFORM = 'Claim Form'
    PENSION = 'Pension Plans'

    # choices for type of information to request
    INFORMATION = (
        (STG, 'Study and Travel Grant'),
        (IVA, 'Institutional Visit Allowance'),
        (DTG, 'Development and Training Grant'),
        (BOOK, 'Book Grant'),
        (CLAIMFORM, 'Claim Form'),
        (PENSION, 'Pension Plans'),
    )
    # link to the user model
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    information = models.CharField(_('Information'), max_length=40, default=STG,
                                   choices=INFORMATION, blank=False)
    message = models.CharField(_('Message'), max_length=255, default='',
                               null=True, blank=True)
    status = models.CharField(max_length=12, default='pending')
    created = models.DateTimeField(verbose_name=_(
        'Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(
        verbose_name=_('Updated'), auto_now=True, null=True)

    class Meta:
        # A human-readable name for the model in the admin panel
        verbose_name = _('Request')

        # A human-readable plural name for the model in the admin panel
        verbose_name_plural = _('Requests')

        # The default sorting order for the model
        ordering = ['-created']

    def __str__(self):
        # A string representation of the model
        return (self.user.first_name+' '+self.user.last_name)

    @property
    def get_full_name(self):
        # A method to get the full name of the user who created the publication
        user = self.user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname+' '+lastname
        return fullname
# create the Employee model


class Employee(models.Model):

    # define gender choices
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

    # define title choices
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

    # define employee type choices
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

    # define the fields for the model
    # PERSONAL DATA
    # link to the user model
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    # title of the employee
    title = models.CharField(_('Title'), max_length=10, default=MR,
                             choices=TITLE, blank=False, null=True)
    # profile picture of the employee
    image = models.ImageField(_('Profile Image'), upload_to='profiles/', default='profiles/default.png',
                              blank=True, null=True, help_text='upload image size less than 2.0MB')
    # first name of the employee
    firstname = models.CharField(
        _('Firstname'), max_length=125, null=False, blank=False)
    # last name of the employee
    lastname = models.CharField(
        _('Lastname'), max_length=125, null=False, blank=False)
    # other name of the employee
    othername = models.CharField(
        _('Othername (optional)'), max_length=125, null=True, blank=True)
    # employee ID
    employeeid = models.PositiveIntegerField(
        _('Employee ID'), null=True, blank=True)
    # gender of the employee
    sex = models.CharField(_('Gender'), max_length=10, default=NOT_KNOWN,
                           choices=GENDER, blank=False)
    # email address of the employee
    email = models.EmailField(
        _('Email'), max_length=255, default=None, blank=True, null=True)
    # phone number of the employee
    tel = PhoneNumberField(null=False, blank=False,
                           verbose_name='Phone Number')
    # biography of the employee
    bio = models.CharField(_('Bio'), max_length=255, default='',
                           null=True, blank=True)
    # date of birth of the employee
    birthday = models.DateField(_('Date of Birth'), blank=False, null=True)
    # NIS number of the employee
    nisnumber = models.PositiveIntegerField(
        _('NIS Number'), null=True, blank=True)
    # type of employment for the employee
    employeetype = models.CharField(_('Employee Type'), max_length=15, default=FULL_TIME,
                                    choices=EMPLOYEETYPE, blank=False, null=True)
    vitae = models.FileField(_('Cirriculum Vitae'), upload_to='vitae/', blank=True,
                             null=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])], help_text='upload in .docx or .pdf')  # curriculum vitae

    """
    is_blocked and is_deleted are boolean fields that indicate whether an employee is blocked or deleted.
    _('Is Blocked') and _('Is Deleted') are translation strings for the field labels.
    """
    is_blocked = models.BooleanField(
        _('Is Blocked'), help_text='button to toggle employee block and unblock', default=False)
    is_deleted = models.BooleanField(
        _('Is Deleted'), help_text='button to toggle employee deleted and undelete', default=False)
    """
    created and updated are datetime fields that store the date and time when an employee is created or updated.
    verbose_name is the human-readable name for the field.
    """
    created = models.DateTimeField(verbose_name=_(
        'Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(
        verbose_name=_('Updated'), auto_now=True, null=True)

    # PLUG MANAGERS
    """
    objects is a reference to the default manager for the model.
    """
    objects = EmployeeManager()

    """
    Meta class contains some metadata for the model.
    verbose_name and verbose_name_plural are human-readable names for the model.
    ordering specifies the default ordering of the records.
    """
    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['-created']

    """
    __str__ method is used to convert the model object to a string representation in the database.
    Here, it returns the full name of the employee using the get_full_name property.
    """

    def __str__(self):
        return self.get_full_name

    """
    get_full_name is a property that returns the full name of the employee.
    It checks if firstname, lastname, and othername fields are available and returns the full name accordingly.
    the @property decorator allows this function to be called as a model property would withoung using '()'
    """
    @ property
    def get_full_name(self):
        fullname = ''
        firstname = self.firstname
        lastname = self.lastname
        othername = self.othername

        if (firstname and lastname) or othername is None:
            fullname = firstname + ' ' + lastname
            return fullname
        elif othername:
            fullname = firstname + ' ' + othername + ' '+lastname
            return fullname
        return

    """
    get_age is a property that returns the age of the employee.
    It calculates the age using the birthday field and the current year.
    """
    @ property
    def get_age(self):
        current_year = datetime.date.today().year
        dateofbirth_year = self.birthday.year
        if dateofbirth_year:
            return current_year - dateofbirth_year
        return

    @ property
    def can_apply_leave(self):
        pass


# Leave Related


class Leave(models.Model):
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

    DAYS = 30  # Default number of leave days per year

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    startdate = models.DateField(verbose_name=_('Start Date'), help_text='leave start date is on ..',
                                 null=True, blank=False)  # Date when the leave period begins
    enddate = models.DateField(verbose_name=_('End Date'), help_text='coming back on ...',
                               null=True, blank=False)  # Date when the leave period ends
    leavetype = models.CharField(
        choices=LEAVE_TYPE, max_length=25, default=SICK, null=True, blank=False)  # Type of leave
    reason = models.CharField(verbose_name=_('Reason for Leave'), max_length=255,
                              help_text='add additional information for leave', null=True, blank=True)  # Optional reason for the leave
    # Number of leave days allocated to the user per year
    defaultdays = models.PositiveIntegerField(verbose_name=_(
        'Leave days per year counter'), default=DAYS, null=True, blank=True)

    # Leave status: pending, approved, rejected, cancelled
    status = models.CharField(max_length=12, default='pending')
    # Flag to indicate if the leave has been approved (not used in this implementation)
    is_approved = models.BooleanField(default=False)

    # Date and time when the leave was last updated
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    # Date and time when the leave was created
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = LeaveManager()  # Custom manager for the Leave model

    class Meta:
        # set the verbose name for this model to 'Leave'
        verbose_name = _('Leave')
        # set the verbose plural name for this model to 'Leaves'
        verbose_name_plural = _('Leaves')
        # set the default ordering of objects to be by 'created' field, in descending order
        ordering = ['-created']

    def __str__(self):
        # define how this object is represented as a string
        return ('{0} - {1}'.format(self.leavetype, self.user))

    @ property
    def pretty_leave(self):
        '''
        A more readable representation of the object, used for display purposes
        '''
        leave = self.leavetype
        user = self.user
        # get the full name of the employee associated with this leave
        employee = user.employee_set.first().get_full_name
        return ('{0} - {1}'.format(employee, leave))

    @ property
    def leave_days(self):
        '''
        Calculate the number of days this leave is for
        '''
        days_count = ''
        startdate = self.startdate
        enddate = self.enddate
        if startdate > enddate:  # if startdate is after enddate, then the dates are invalid
            return
        dates = (enddate - startdate)
        return dates.days

    @ property
    def leave_approved(self):
        '''
        Check if this leave has been approved or not
        '''
        return self.is_approved == True

    @ property
    def approve_leave(self):
        '''
        Approve this leave request
        '''
        if not self.is_approved:
            self.is_approved = True
            self.status = 'approved'
            self.save()

    @ property
    def unapprove_leave(self):
        '''
        Unapprove this leave request
        '''
        if self.is_approved:
            self.is_approved = False
            self.status = 'pending'
            self.save()

    @ property
    def leaves_cancel(self):
        '''
        Cancel this leave request
        '''
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = 'cancelled'
            self.save()

    @ property
    def uncancel_leave(self):
        '''
        Revert the cancellation of this leave request
        '''
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = 'pending'
            self.save()

    @ property
    def reject_leave(self):
        '''
        Reject this leave request
        '''
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = 'rejected'
            self.save()

    @ property
    def is_rejected(self):
        '''
        Check if this leave request has been rejected
        '''
        return self.status == 'rejected'

    @ property
    def get_full_name(self):
        '''
        Get the full name of the user associated with this leave request
        '''
        user = self.user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname+' '+lastname
        return fullname


class Publications(models.Model):
    # Constants representing the different types of publications
    JOURNAL = 'Peer Reviewed Journal'
    CONFERENCE = 'Conference Paper'
    BOOK = 'Book'

    # A tuple of choices for the publication type field
    PUBLICATION_TYPE = (
        (JOURNAL, 'Peer Reviewed Journal'),
        (CONFERENCE, 'Conference Paper'),
        (BOOK, 'Book'),
    )

    # A foreign key to the CustomUser model
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)

    # A character field to represent the title of the publication
    title = models.CharField(max_length=100, verbose_name=_(
        'Title'), null=True, blank=False)

    # A character field to represent the academic year of the publication
    year = models.CharField(verbose_name=_(
        'Academic Year'), null=True, blank=False, max_length=9)

    # A character field to represent the type of the publication
    publicationtype = models.CharField(_('Publication Type'), max_length=25, default=JOURNAL,
                                       choices=PUBLICATION_TYPE, blank=False, null=True)

    # A date time field representing when the publication was last updated
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    # A date time field representing when the publication was created
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    # A custom manager for the Publications model
    objects = PublicationManager()

    class Meta:
        # A human-readable name for the model in the admin panel
        verbose_name = _('Publication')

        # A human-readable plural name for the model in the admin panel
        verbose_name_plural = _('Publications')

        # The default sorting order for the model
        ordering = ['-created']

    def __str__(self):
        # A string representation of the model
        return (self.user.first_name+' '+self.user.last_name)

    @property
    def get_full_name(self):
        # A method to get the full name of the user who created the publication
        user = self.user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname+' '+lastname
        return fullname


class Awards(models.Model):
    # A foreign key that refers to the user who received the award
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100, verbose_name=_(
        'Title'), null=True, blank=False)  # A field that stores the title of the award
    # A field that stores the year the award was received
    year = models.CharField(verbose_name=_(
        'Academic Year'), null=True, blank=False, max_length=9)
    # A field that stores the last time the record was updated
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    # A field that stores the time the record was created
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        # A human-readable name for a single instance of the model
        verbose_name = _('Award')
        # A human-readable name for multiple instances of the model
        verbose_name_plural = _('Awards')
        ordering = ['-created']  # The default ordering for the model

    def __str__(self):
        # Returns the full name of the user who received the award as a string
        return (self.user.first_name+' '+self.user.last_name)

    @property
    def get_full_name(self):
        user = self.user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname+' '+lastname
        return fullname


class Conferences(models.Model):
    # link to user who attended conference
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100, verbose_name=_(
        'Title'), null=True, blank=False)  # title of conference
    year = models.CharField(verbose_name=_(
        'Academic Year'), null=True, blank=False, max_length=9)  # year of conference
    updated = models.DateTimeField(
        auto_now=True, auto_now_add=False)  # last updated timestamp
    created = models.DateTimeField(
        auto_now=False, auto_now_add=True)  # created timestamp

    class Meta:
        verbose_name = _('Conference')  # singular name of the model
        verbose_name_plural = _('Conferences')  # plural name of the model
        ordering = ['-created']  # order by most recent conferences first

    def __str__(self):
        # string representation of the object
        return (self.user.first_name+' '+self.user.last_name)

    @property
    def get_full_name(self):
        user = self.user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname+' '+lastname
        return fullname  # get the full name of the user who attended the conference


class Development(models.Model):
    # foreign key to the user model
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    # title of the development
    title = models.CharField(max_length=100, verbose_name=_(
        'Title'), null=True, blank=False)
    # starting year of the development
    year_start = models.IntegerField(verbose_name=_('Start Year'), null=True, validators=[
        MinValueValidator(1900), max_value_current_year])
    # ending year of the development
    year_end = models.IntegerField(verbose_name=_('End Year'), null=True, validators=[
        MinValueValidator(1900), max_value_current_year])
    # timestamp for last update
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    # timestamp for creation
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _('Development')
        verbose_name_plural = _('Development')
        ordering = ['-created']

    def __str__(self):
        return (self.user.first_name+' '+self.user.last_name)

    @ property
    def get_full_name(self):
        # return the full name of the user associated with the development
        user = self.user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname+' '+lastname
        return fullname


class Manuscripts(models.Model):
    IN_PREPARATION = 'in preparation'
    IN_REVIEW = 'under review'

    STATUS = (
        (IN_PREPARATION, 'in preparation'),
        (IN_REVIEW, 'under review'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100, verbose_name=_(
        'Title'), null=True, blank=False)
    status = models.CharField(_('Status'), max_length=25, default=IN_PREPARATION,
                              choices=STATUS, blank=False, null=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _('Manuscript')
        verbose_name_plural = _('Manuscripts')
        ordering = ['-created']

    def __str__(self):
        # Return the full name of the user
        return (self.user.first_name+' '+self.user.last_name)

    @property
    def get_full_name(self):
        # Return the full name of the user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname+' '+lastname
        return fullname


class Presentations(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100, verbose_name=_(
        'Title'), null=True, blank=False)
    year = models.CharField(verbose_name=_(
        'Academic Year'), null=True, blank=False, max_length=9)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _('Presentation')
        verbose_name_plural = _('Presentations')
        ordering = ['-created']

    def __str__(self):
        # Return the full name of the user
        return (self.user.first_name+' '+self.user.last_name)

    @property
    def get_full_name(self):
        # Return the full name of the user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname+' '+lastname
        return fullname


class Consultancies(models.Model):
    # The user who created the consultancy
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)

    # The title of the consultancy
    title = models.CharField(max_length=100, verbose_name=_(
        'Title'), null=True, blank=False)

    # The position of the user in the consultancy
    position = models.CharField(max_length=50, verbose_name=_(
        'Position'), null=True, blank=True)

    # The period of the consultancy
    period = models.CharField(verbose_name=_(
        'Period'), null=True, max_length=50)

    # The date and time when the consultancy was last updated
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    # The date and time when the consultancy was created
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        # The singular name of the model
        verbose_name = _('Consultancy')
        # The plural name of the model
        verbose_name_plural = _('Consultancies')
        # The default ordering for the model
        ordering = ['-created']

    def __str__(self):
        # The string representation of the consultancy
        return (self.user.first_name+' '+self.user.last_name)

    @ property
    def get_full_name(self):
        # The full name of the user who created the consultancy
        user = self.user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname+' '+lastname
        return fullname


class Grants(models.Model):
    # User who created the grant
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100, verbose_name=_(
        'Title'), null=True, blank=False)  # Title of the grant
    # Date and time the grant was last updated
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    # Date and time the grant was created
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _('Grant')  # Singular name of the model
        verbose_name_plural = _('Grants')  # Plural name of the model
        # Order grants by creation date in descending order
        ordering = ['-created']

    def __str__(self):
        # Return the name of the user who created the grant
        return (self.user.first_name + ' ' + self.user.last_name)

    @property
    def get_full_name(self):
        user = self.user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname + ' ' + lastname
        return fullname  # Return the full name of the user who created the grant

# university public and professional service roles


class Roles(models.Model):
    # User who created the role
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    role = models.CharField(max_length=100, verbose_name=_(
        'Role'), null=True, blank=False)  # name of the role
    association = models.CharField(max_length=100, verbose_name=_(
        'Association'), null=True, blank=False)  # associaiton of the role
    date = models.DateField(_('Date'), blank=False, null=True)
    # Date and time the entry was last updated
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    # Date and time the entry was created
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _('Role')  # Singular name of the model
        verbose_name_plural = _('Roles')  # Plural name of the model
        # Order grants by creation date in descending order
        ordering = ['-created']

    def __str__(self):
        # Return the name of the user who created the entry
        return (self.user.first_name + ' ' + self.user.last_name)

    @property
    def get_full_name(self):
        user = self.user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname + ' ' + lastname
        return fullname  # Return the full name of the user who created the entry


class Research(models.Model):
    # User who created the entry
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    research = models.CharField(max_length=200, verbose_name=_(
        'Research'), null=True, blank=False)  # name of the research
    interest = models.CharField(max_length=200, verbose_name=_(
        'Interest'), null=True, blank=False)  # interest in the research

    # Date and time the entry was last updated
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    # Date and time the entry was created
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _('Research')  # Singular name of the model
        verbose_name_plural = _('Research')  # Plural name of the model
        # Order grants by creation date in descending order
        ordering = ['-created']

    def __str__(self):
        # Return the name of the user who created the entry
        return (self.user.first_name + ' ' + self.user.last_name)

    @property
    def get_full_name(self):
        user = self.user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname + ' ' + lastname
        return fullname  # Return the full name of the user who created the entry


class Supervision(models.Model):

    levels = ((1, 1), (2, 2), (3, 3), (4, 4,), (5, 5))
    # User who created the entry
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)

    # first name of the student supervised
    firstname = models.CharField(
        _('Student First name'), max_length=125, null=False, blank=False)
    # last name of the student supervised
    lastname = models.CharField(
        _('Student Last name'), max_length=125, null=False, blank=False)
    # degree level of the student
    level = models.IntegerField(
        _('Student Degree Level'), blank=False, null=True, choices=levels, default=1)
    title = models.CharField(max_length=100, verbose_name=_(
        'Project/Thesis Title'), null=True, blank=False)  # title of the thesis or project
    # academic year of the project /thesis
    year = models.CharField(verbose_name=_(
        'Academic Year'), null=True, blank=False, max_length=9)
    # Date and time the entry was last updated
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    # Date and time the entry was created
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _('Supervision')  # Singular name of the model
        verbose_name_plural = _('Supervision')  # Plural name of the model
        # Order grants by creation date in descending order
        ordering = ['-created']

    def __str__(self):
        # Return the name of the user who created the entry
        return (self.user.first_name + ' ' + self.user.last_name)

    @property
    def get_full_name(self):
        user = self.user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname + ' ' + lastname
        return fullname  # Return the full name of the user who created the entry


class Specialisation(models.Model):
    # User who created the entry
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    area = models.CharField(max_length=100, verbose_name=_(
        'Area'), null=True, blank=False)  # area of academic specialisation

    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    # Date and time the entry was created
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _('Specialisation')  # Singular name of the model
        verbose_name_plural = _('Specialisation')  # Plural name of the model
        # Order grants by creation date in descending order
        ordering = ['-created']

    def __str__(self):
        # Return the name of the user who created the entry
        return (self.user.first_name + ' ' + self.user.last_name)

    @property
    def get_full_name(self):
        user = self.user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname + ' ' + lastname
        return fullname  # Return the full name of the user who created the entry

 # Other professional activities


class Activities(models.Model):
    # User who created the entry
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    activity = models.CharField(max_length=200, verbose_name=_(
        'Professional Activities'), null=True, blank=False)  # profession activity

    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    # Date and time the entry was created
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _('Activity')  # Singular name of the model
        verbose_name_plural = _('Activities')  # Plural name of the model
        # Order grants by creation date in descending order
        ordering = ['-created']

    def __str__(self):
        # Return the name of the user who created the entry
        return (self.user.first_name + ' ' + self.user.last_name)

    @property
    def get_full_name(self):
        user = self.user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname + ' ' + lastname
        return fullname  # Return the full name of the user who created the entry

# Honours and ceritficates


class Honours(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100, verbose_name=_(
        'Title'), null=True, blank=False)  # title of the honour or certificate
    competition = models.CharField(max_length=100, verbose_name=_(
        'Competition'), null=True, blank=True)  # name of the competition
    year = models.CharField(verbose_name=_(
        'Academic Year'), null=True, blank=False, max_length=9)
    # Date and time the entry was last updated
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    # Date and time the entry was created
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _('Honour')  # Singular name of the model
    verbose_name_plural = _('Honours')  # Plural name of the model
    # Order grants by creation date in descending order
    ordering = ['-created']

    def __str__(self):
        # Return the name of the user who created the entry
        return (self.user.first_name + ' ' + self.user.last_name)

    @property
    def get_full_name(self):
        user = self.user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname + ' ' + lastname
        return fullname  # Return the full name of the user who created the entry

# Contribution to the department, faculty or university


class Contributions(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    contribution = models.CharField(max_length=100, verbose_name=_(
        'Contribution'), null=True, blank=False)  # Contribution to the department, faculty or university
    year = models.CharField(verbose_name=_(
        'Academic Year'), null=True, blank=False, max_length=9)
    # Date and time the entry was last updated
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    # Date and time the entry was created
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _('Contirbution')  # Singular name of the model
    verbose_name_plural = _('Contributions')  # Plural name of the model
    # Order grants by creation date in descending order
    ordering = ['-created']

    def __str__(self):
        # Return the name of the user who created the entry
        return (self.user.first_name + ' ' + self.user.last_name)

    @property
    def get_full_name(self):
        user = self.user
        firstname = self.user.first_name
        lastname = self.user.last_name
        fullname = firstname + ' ' + lastname
        return fullname  # Return the full name of the user who created the entry
