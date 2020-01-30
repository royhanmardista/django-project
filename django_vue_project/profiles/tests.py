from django.test import TestCase

# Create your tests here.
# Create your tests here.
class LowonganListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"

        self.company_name = "lorem_ipsum"
        self.company_description = "lorem ipsum dolor sit amet"
        self.company_address = "Jl Jalan"
        self.company_contact = "johny bravo - 08123456789"

        self.job_title = "test job"
        self.job_description = "lorem ipsum dolor sit amet"

        self.user = User.objects.create_user(
            self.username, self.email, self.password
        )

        self.user_perusahaan = UserPerusahaan.objects.create(
            user=self.user,
            nama=self.company_name,
        )

        self.company = Perusahaan()
        self.company.name = self.company_name,
        self.company.description = self.company_description,
        self.company.address = self.company_address,
        self.company.contact_person = self.company_contact,
        self.company.save()

        self.user_perusahaan = self.company

        self.job = Job.objects.create(
            perusahaan=self.company,
            position=self.job_title,
            description=self.job_description,
        )

        self.url = reverse("lowongan:list")
        self.company_url = reverse(
            "lowongan:detail", kwargs={
                "pk": self.company.pk})