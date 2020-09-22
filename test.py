import requests
import json


class Error(Exception):
    def __init__(self):
        self.error_name = self.__class__.__name__
        self.error_message = ""
        self.error_details = ""

    def __str__(self, *args, **kwargs):
        error_json = {}
        if self.error_name:
            error_json["name"] = self.error_name

        if self.error_message:
            error_json["message"] = self.error_message

        if self.error_details:
            error_json["details"] = self.error_details

        return json.dumps(error_json)


class DataAttrNotExistsError(Error):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.error_message = "Data Attribute not exists in the Search Movies GET Requests"


class TotalPagesAttrNotExistsError(Error):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.error_message = "TotalPages Attribute not exists in the Search Movies GET Requests"


class PageNumberAttrNotExistsError(Error):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.error_message = "PageNumber Attribute not exists in the Search Movies GET Requests"


class TitleAttrNotExistsError(Error):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.error_message = "Title Attribute not exists in the Search Movies GET Requests"


class HTTPError(Error):
    def __init__(self, statusCode):
        super(self.__class__, self).__init__()
        self.statusCode = statusCode


class MoviesAPI:
    def __init__(self):
        # Search Movie URL
        self.__searchMoviesURL = 'https://jsonmock.hackerrank.com/api/movies/search/?Title={substr}&page={pageNumber}'

        # Attributes
        self.titleAttr = 'Title'
        self.pageNumberAttr = 'page'
        self.totalPagesNumberAttr = 'total_pages'
        self.dataAttr = 'data'

        # Creating Session
        self.__request = requests.Session()

    def search_movie_get_request(self, subString, pageNumber=1):
        try:
            url = self.__searchMoviesURL.format(substr=subString, pageNumber=pageNumber)
            response = self.__request.get(url)
            response.raise_for_status()
            data = response.json()
            if self.totalPagesNumberAttr not in data:
                raise TotalPagesAttrNotExistsError

            if self.pageNumberAttr not in data:
                raise PageNumberAttrNotExistsError

            if self.dataAttr not in data:
                raise DataAttrNotExistsError

            return data

        except requests.exceptions.HTTPError:
            raise HTTPError(response.status_code)

        except DataAttrNotExistsError as e:
            raise DataAttrNotExistsError

        except TotalPagesAttrNotExistsError as e:
            raise TotalPagesAttrNotExistsError

        except PageNumberAttrNotExistsError as e:
            raise TotalPagesAttrNotExistsError

        except Exception as e:
            raise e


def getMovieTitles(substr):
    try:
        moviesAPIObj = MoviesAPI()
        fetchedTitles = []

        movies = moviesAPIObj.search_movie_get_request(subString=substr)

        for movie in movies[moviesAPIObj.dataAttr]:
            if moviesAPIObj.titleAttr not in movie:
                raise TitleAttrNotExistsError
            fetchedTitles.append(movie[moviesAPIObj.titleAttr])

        while int(movies[moviesAPIObj.pageNumberAttr]) < int(movies[moviesAPIObj.totalPagesNumberAttr]):
            movies = moviesAPIObj.search_movie_get_request(subString=substr, pageNumber=int(movies[moviesAPIObj.pageNumberAttr]) + 1)
            for movie in movies[moviesAPIObj.dataAttr]:
                if moviesAPIObj.titleAttr not in movie:
                    raise TitleAttrNotExistsError
                fetchedTitles.append(movie[moviesAPIObj.titleAttr])

        fetchedTitles.sort()

        return fetchedTitles

    except HTTPError as e:
        r = json.dumps({'status': False, 'status_code': e.statusCode})
        return r

    except DataAttrNotExistsError as e:
        r = json.dumps({'status': False, 'message': str(e.error_message)})
        return r

    except TotalPagesAttrNotExistsError as e:
        r = json.dumps({'status': False, 'message': str(e.error_message)})
        return r

    except PageNumberAttrNotExistsError as e:
        r = json.dumps({'status': False, 'message': str(e.error_message)})
        return r

    except Exception as e:
        r = json.dumps({'status': False, 'message': str(e)})
        return r


