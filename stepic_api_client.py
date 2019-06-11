# Run with Python 3
import requests
import csv


class Course:
    """ Класс курса. Все данные и свойства курса представлены в виде атрибутов класса для более удобного доступа.
        Удобно, если работаете с небольшим количеством курсов и с определенными данными. """

    def __init__(self, course_info: dict):

        self.id = course_info["id"]
        self.summary = course_info["summary"]
        self.workload = course_info["workload"]
        self.course_format = course_info["course_format"]
        self.target_audience = course_info["target_audience"]
        self.is_certificate_issued = course_info["is_certificate_issued"]
        self.is_certificate_auto_issued = course_info["is_certificate_auto_issued"]
        self.certificate_regular_threshold = course_info["certificate_regular_threshold"]
        self.certificate_distinction_threshold = course_info["certificate_distinction_threshold"]
        self.instructors = course_info["instructors"]
        self.certificate = course_info["certificate"]
        self.requirements = course_info["requirements"]
        self.description = course_info["description"]
        self.sections = course_info["sections"]
        self.total_units = course_info["total_units"]
        self.first_deadline = course_info["first_deadline"]
        self.last_deadline = course_info["last_deadline"]
        self.subscriptions = course_info["subscriptions"]
        self.announcements = course_info["announcements"]
        self.is_contest = course_info["is_contest"]
        self.is_self_paced = course_info["is_self_paced"]
        self.is_adaptive = course_info["is_adaptive"]
        self.authors = course_info["authors"]
        self.tags = course_info["tags"]
        self.has_tutors = course_info["has_tutors"]
        self.is_enabled = course_info["is_enabled"]
        self.is_proctored = course_info["is_proctored"]
        self.proctor_url = course_info["proctor_url"]
        self.review_summary = course_info["review_summary"]
        self.certificates_count = course_info["certificates_count"]
        self.learners_count = course_info["learners_count"]
        self.lessons_count = course_info["lessons_count"]
        self.quizzes_count = course_info["quizzes_count"]
        self.challenges_count = course_info["challenges_count"]
        self.videos_duration = course_info["videos_duration"]
        self.time_to_complete = course_info["time_to_complete"]
        self.is_popular = course_info["is_popular"]
        self.similar_courses = course_info["similar_courses"]
        self.is_paid = course_info["is_paid"]
        self.price = course_info["price"]
        self.is_archived = course_info["is_archived"]
        self.language = course_info["language"]
        self.is_featured = course_info["is_featured"]
        self.is_public = course_info["is_public"]
        self.title = course_info["title"]
        self.slug = course_info["slug"]
        self.is_active = course_info["is_active"]
        self.create_date = course_info["create_date"]
        self.update_date = course_info["update_date"]

    def select_info(self, info_name: list):
        """ Функция, которая принимает список с названиями атрибутов
            и возвращает словарь со значениями этих атрибутов."""

        sorted_dict = {}

        for info in info_name:
            sorted_dict[info] = self.__dict__[info]

        return sorted_dict


class StepikClient:

    def __init__(self, client_id, client_secret):

        self.client_id = client_id
        self.client_secret = client_secret

        auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        self.auth = auth

        response = requests.post('https://stepik.org/oauth2/token/',
                                 data={'grant_type': 'client_credentials'},
                                 auth=auth)
        self.response = response

        token = response.json().get('access_token', None)
        if not token:
            print('Unable to authorize with provided credentials')
            exit(1)
        else:
            print("Authorization was successful!")
        self.token = token

    def get_course(self, course_id: int, progress=True):

        api_url = f'https://stepik.org/api/courses/{course_id}'

        course = requests.get(api_url,
                              headers={'Authorization': 'Bearer ' + self.token}).json()

        course = course["courses"]
        course = Course(course[0])

        if progress:
            print(f"Course {course_id} done!")

        return course

    def get_many_courses(self, courses_ids: list, fail_flag=True):

        courses = []
        fails = []

        for course in courses_ids:
            try:
                courses.append(self.get_course(course))
            except:
                fails.append(f"Course {course} was failed!")

        if fail_flag:
            for message in fails:
                print(message)

        return courses


def write_csv(path: str, fieldnames: list, data: list):
    """ функция для записи данных в csv-файл.
        path - путь и имя файла
        fieldnames - список с названиями для колонок
        data - данные, которые нужно записать""" 

    with open(path, "a", newline='') as out_file:

        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row.__dict__)


if __name__ == "__main__":
    # импортируем отдельный файл, в котором храним id и secret
    from stepic_client import CLIENT_ID, CLIENT_SECRET
    
    # создаем экземпляр клиента, производится аутентификация
    client = StepikClient(CLIENT_ID, CLIENT_SECRET)
    
    # скачиваем данные определенного курса по его id
    my_course = client.get_course(67)
    
    # скачиваем данные нескольких курсов по их id
    course_list = test.get_many_courses([67,512, 401,50352])
    
    # создаем список с названиям для колонок по ключам из класса Course
    columns = list(my_course.__dict__.keys())
    
    # скачиваем данные курсов с id c 1000 по 1500
    # fail_flag = False - если данные не удалось скачать, то НЕ выводить сообщение о неудаче
    first_courses = test.get_many_courses(range(1000,1500), fail_flag=False)

    # записываем полученные данные в файл csv для дальнейшей обработки
    write_csv("test.csv", columns, first_courses)


