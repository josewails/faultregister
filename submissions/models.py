from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Originator(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    area = models.ForeignKey(Area, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name


class Supervisor(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name


class IssueCategory(models.Model):
    name = models.CharField(max_length=256)


class IssueDetails(models.Model):
    category = models.ForeignKey(IssueCategory, related_name='issues', on_delete=models.CASCADE, null=True)
    part_or_assembly_image = models.URLField(null=True)
    part_or_assembly_detail = models.URLField(null=True)
    accurate_description = models.TextField(null=True, blank=True)
    exact_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.category.name


class Classification(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class FaultSource(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class NotificationRecipient(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class MachineType(models.Model):
    letter = models.CharField(max_length=5)

    def __str__(self):
        return self.letter


class SubmissionStatus(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class SubmissionProgress(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class MachineClassification(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class TestType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Submission(models.Model):
    submission_id = models.CharField(max_length=64)
    machine_shop_update = models.DateTimeField(null=True)
    quality_update = models.DateTimeField(null=True)
    stores_update = models.DateTimeField(null=True)
    cs_stores_update = models.DateTimeField(null=True)
    time_to_close = models.FloatField(null=True)
    originator = models.ForeignKey(Originator, blank=True, null=True, related_name='submissions',
                                   on_delete=models.SET_NULL)
    fault_source = models.ForeignKey(FaultSource, null=True, blank=True, related_name='submissions',
                                     on_delete=models.SET_NULL)
    time_in_quality = models.FloatField(null=True, blank=True)
    time_in_stores = models.FloatField(null=True, blank=True)
    time_in_cs_stores = models.FloatField(null=True, blank=True)
    scan_qr_code = models.IntegerField(null=True, blank=True)
    supervisor = models.ForeignKey(Supervisor, blank=True, null=True, related_name='submissions',
                                   on_delete=models.SET_NULL)
    input_start_date = models.DateTimeField(blank=True, null=True)
    part_number = models.CharField(max_length=256, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    total_part_cost = models.FloatField(null=True, blank=True)
    order_number = models.IntegerField(null=True, blank=True)

    rework_quantity = models.IntegerField(null=True, blank=True)
    scrap_quantity = models.IntegerField(null=True, blank=True)
    stock_quantity = models.IntegerField(null=True, blank=True)
    to_be_reworked_on_site = models.BooleanField(blank=True, null=True)
    notification_recipient = models.ForeignKey(NotificationRecipient, null=True, blank=True, related_name='submissions',
                                               on_delete=models.SET_NULL)
    part_description = models.TextField(null=True, blank=True)
    bin_number = models.CharField(max_length=64, null=True, blank=True)
    unit_part_cost = models.FloatField(null=True, blank=True)
    total_ncr_cost = models.FloatField(null=True, blank=True)
    classification = models.ForeignKey(Classification, null=True, blank=True, related_name='submissions',
                                       on_delete=models.SET_NULL)
    production_order_number = models.CharField(max_length=64, null=True, blank=True)
    machine_number = models.CharField(max_length=64, null=True, blank=True)
    machine_type = models.ForeignKey(MachineType, null=True, blank=True, on_delete=models.SET_NULL)
    machine_classification = models.ForeignKey(MachineClassification, null=True, blank=True, on_delete=models.SET_NULL)
    test_type = models.ForeignKey(TestType, null=True, blank=True, on_delete=models.SET_NULL)
    vendor_id = models.CharField(max_length=64, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, null=True, blank=True, related_name='submissions',
                                 on_delete=models.SET_NULL)
    issue_details = models.ForeignKey(IssueDetails, null=True, blank=True, related_name='submissions',
                                      on_delete=models.SET_NULL)
    previous_area = models.ForeignKey(Area, null=True, blank=True, related_name='previous_area_submissions',
                                      on_delete=models.SET_NULL)
    current_area = models.ForeignKey(Area, null=True, blank=True, related_name='current_area_submissions',
                                     on_delete=models.SET_NULL)
    sap_updated = models.BooleanField(null=True, blank=True)
    rework_time = models.FloatField(null=True, blank=True)
    serial_number = models.CharField(max_length=576, null=True, blank=True)
    create_an_ncr = models.BooleanField(null=True, blank=True)
    caq_ncr = models.CharField(max_length=256, null=True, blank=True)
    status = models.ForeignKey(SubmissionStatus, null=True, blank=True, related_name='submissions',
                               on_delete=models.CASCADE)
    defect_origin_area = models.ForeignKey(Area, blank=True, null=True, on_delete=models.CASCADE,
                                           related_name='defect_submissions')
    minutes_wasted = models.IntegerField(null=True, blank=True)
    remark = models.CharField(max_length=256, null=True, blank=True)
    eight_d_requested = models.BooleanField(blank=True, null=True)
    eight_d_supplied = models.BooleanField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=128, null=True, blank=True)
    progress = models.ForeignKey(SubmissionProgress, null=True, on_delete=models.SET_NULL, related_name='submissions',
                                 blank=True)
    draft = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.submission_id
