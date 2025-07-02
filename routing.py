import re


# route = input("Enter your route:\n")

routes = ['/books/:isbn', '/books', '/borrow/:borrowid', '/books/language/:language']
route_regexes = []


def regex_generator(URI):
    path_regex = "^" + re.sub(r":\w+", "\\\\w+", URI) + "$"
    return path_regex

for route in routes:
    print(regex_generator(route))
    route_regexes.append(regex_generator(route))
print(f"This is the list of regex routes we have: {route_regexes}")

URL = input("Enter your url:\n")

for route_regex in route_regexes:
    if re.match(regex_generator(route_regex), URL) is not None:
        print(f"We can server this route: with this {route_regex}")

