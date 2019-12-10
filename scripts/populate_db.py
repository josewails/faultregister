import os
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from apscheduler.schedulers.blocking import BlockingScheduler

# use creds to create a client to interact with Google Drive API

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('google_client_secret.json', scope)
client = gspread.authorize(creds)

# initialize the scheduler

scheduler = BlockingScheduler()

from submissions.models import (
    Area, Submission, SubmissionStatus, Supervisor, Supplier, FaultSource, Classification,
    Originator, MachineType, IssueDetails, NotificationRecipient, SubmissionProgress, MachineClassification, TestType,
    IssueCategory
)

base_dir = os.path.dirname(os.path.abspath(__file__))
sheet = client.open_by_url(
    'https://docs.google.com/spreadsheets/d/1HWZDi2TdwV5IpTym5B3QAydFCRIv88NsRtVVvSswMgI/edit#gid=615674405').sheet1


class PopulateDB:

    def __init__(self):

        self.records = sheet.get_all_records()
        self.columns = [key for key in self.records[0]]

    @staticmethod
    def process_yes_no(answer):

        """

        Receives 'Yes' or 'No' and converts that to a bool
        :param answer:
        :return:
        """

        if answer is 'Yes':
            return True

        if answer is 'No':
            return False

        return None

    def process_row(self, row):

        originator_area, _ = Area.objects.get_or_create(name=row[self.columns[7]])
        originator, _ = Originator.objects.get_or_create(
            first_name=row[self.columns[6]].split()[0]
        )

        if len(row[self.columns[6]].split()) > 1:
            originator.last_name = row[self.columns[6]].split()[1].strip()

        originator.area = originator_area
        originator.save()

        fault_source, _ = FaultSource.objects.get_or_create(name=row[self.columns[8]])

        # Create a supervisor

        supervisor, _ = Supervisor.objects.get_or_create(name=row[self.columns[14]])
        if row[self.columns[15]]:
            supervisor.email = row[self.columns[15]]
            supervisor.save()

        submission, _ = Submission.objects.get_or_create(
            submission_id=row[self.columns[0]]
        )

        submission_data = dict(
            submission_id=row[self.columns[0]],
            machine_shop_update=datetime.datetime.strptime(row[self.columns[1]], '%Y-%m-%d %H:%M:%S') if row[
                self.columns[1]] else None,
            quality_update=datetime.datetime.strptime(row[self.columns[2]], '%Y-%m-%d %H:%M:%S') if row[
                self.columns[2]] else None,
            stores_update=datetime.datetime.strptime(row[self.columns[3]], '%Y-%m-%d %H:%M:%S') if row[
                self.columns[3]] else None,
            cs_stores_update=datetime.datetime.strptime(row[self.columns[4]], '%Y-%m-%d %H:%M:%S') if row[
                self.columns[4]] else None,
            time_to_close=row[self.columns[5]] if row[self.columns[5]] else None,
            originator=originator,
            fault_source=fault_source,
            time_in_quality=row[self.columns[9]] if isinstance(row[self.columns[9]], float) else None,
            time_in_stores=row[self.columns[10]] if isinstance(row[self.columns[10]], float) else None,
            time_in_cs_stores=row[self.columns[11]] if isinstance(row[self.columns[11]], float) else None,
            scan_qr_code=row[self.columns[12]] if isinstance(row[self.columns[12]], int) else None,
            supervisor=supervisor,
            input_start_date=datetime.datetime.strptime(row[self.columns[16]], '%Y-%m-%d %H:%M:%S'),
            part_number=row[self.columns[17]],
            quantity=row[self.columns[18]] if isinstance(row[self.columns[18]], int) else None,
            total_part_cost=row[self.columns[19]] if isinstance(row[self.columns[19]], int) else None,
            order_number=row[self.columns[20]] if isinstance(row[self.columns[20]], int) else None,
            rework_quantity=row[self.columns[21]] if isinstance(row[self.columns[21]], int) else None,
            scrap_quantity=row[self.columns[22]] if isinstance(row[self.columns[22]], int) else None,
            stock_quantity=row[self.columns[23]] if isinstance(row[self.columns[23]], int) else None,
            to_be_reworked_on_site=self.process_yes_no(row[self.columns[24]]),
            part_description=row[self.columns[26]],
            bin_number=row[self.columns[27]],
            unit_part_cost=row[self.columns[28]] if isinstance(row[self.columns[28]], float) else None,
            total_ncr_cost=row[self.columns[29]] if isinstance(row[self.columns[29]], float) else None,
            production_order_number=row[self.columns[31]],
            machine_number=row[self.columns[32]],
            vendor_id=row[self.columns[36]],
            sap_updated=self.process_yes_no(row[self.columns[47]]),
            rework_time=row[self.columns[48]] if isinstance(row[self.columns[48]], float) else None,
            serial_number=row[self.columns[49]],
            create_an_ncr=self.process_yes_no(row[self.columns[50]]),
            caq_ncr=row[self.columns[51]] if row[self.columns[51]] else None,
            minutes_wasted=row[self.columns[54]] if isinstance(row[self.columns[54]], int) else None,
            remark=row[self.columns[55]],
            eight_d_requested=self.process_yes_no(row[self.columns[56]]),
            eight_d_supplied=self.process_yes_no(row[self.columns[57]]),
            last_updated_by=row[self.columns[58]],
            draft=row[self.columns[60]]
        )

        for field, value in submission_data.items():
            setattr(submission, field, value)

        if row[self.columns[25]]:
            notification_recipient, _ = NotificationRecipient.objects.get_or_create(name=row[self.columns[25]])
            submission.notification_recipient = notification_recipient

        if row[self.columns[30]]:
            classification, _ = Classification.objects.get_or_create(name=row[self.columns[30]])
            submission.classification = classification

        if row[self.columns[37]]:
            supplier, _ = Supplier.objects.get_or_create(name=row[self.columns[37]])

            if row[self.columns[38]]:
                supplier.email = row[self.columns[38]]
                supplier.save()

            submission.supplier = supplier

        if row[self.columns[32]]:
            machine_type, _ = MachineType.objects.get_or_create(letter=row[self.columns[33]])
            submission.machine_type = machine_type

        if row[self.columns[34]]:
            machine_classification, _ = MachineClassification.objects.get_or_create(name=row[self.columns[34]])
            submission.machine_classification = machine_classification

        if row[self.columns[35]]:
            test_type, _ = TestType.objects.get_or_create(name=row[self.columns[35]])
            submission.test_type = test_type

        if row[self.columns[41]]:
            issue_category, _ = IssueCategory.objects.get_or_create(name=row[self.columns[41]])

            if row[self.columns[39]] or row[self.columns[40]] or row[self.columns[42]] or row[self.columns[43]]:
                issue_details = IssueDetails.objects.create(
                    category=issue_category,
                    part_or_assembly_image=row[self.columns[39]],
                    part_or_assembly_detail=row[self.columns[40]],
                    accurate_description=row[self.columns[42]],
                    exact_description=row[self.columns[43]]
                )
                submission.issue_details = issue_details

        if row[self.columns[45]]:
            previous_area, _ = Area.objects.get_or_create(name=row[self.columns[45]])
            submission.previous_area = previous_area

        if row[self.columns[46]]:
            current_area, _ = Area.objects.get_or_create(name=row[self.columns[46]])
            submission.current_area = current_area

        if row[self.columns[52]]:
            status, _ = SubmissionStatus.objects.get_or_create(name=row[self.columns[52]])
            submission.status = status

        if row[self.columns[53]]:
            defect_origin_area, _ = Area.objects.get_or_create(name=row[self.columns[53]])
            submission.defect_origin_area = defect_origin_area

        if row[self.columns[59]]:
            progress, _ = SubmissionProgress.objects.get_or_create(name=row[self.columns[59]])
            submission.progress = progress

        submission.save()

    def process_rows_subset(self, indices_chunk):

        for index in indices_chunk:
            row = self.records[index]
            print(f"Processing row #{index}")
            self.process_row(row)

    def process_submission_data(self, chunk_size):

        """
        This function will grab
        :return:
        """

        records = self.records

        num_records = len(records)
        row_indices = [_ for _ in range(num_records)]
        row_indices_chunks = [row_indices[i:i + chunk_size] for i in range(0, len(records), chunk_size)]

        for chunk in row_indices_chunks:
            self.process_rows_subset(chunk)


def populate():
    populate_db = PopulateDB()
    populate_db.process_submission_data(2)


def schedule_populate():
    scheduler.add_job(populate, 'interval', hours=12)
    scheduler.start()


def run():
    populate()
