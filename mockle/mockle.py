import os
import just


def get_env():
    return os.environ.get("PYTHON_ENV", "prod")

print("mockle env", get_env())


def get_path(name):
    if not os.path.isdir("./.mockle"):
        os.makedirs("./.mockle")
    return os.path.join("./.mockle", name + ".pkl")


def mockle(name, good=None, exception=""):
    name = get_path(name)
    if get_env() == "dev":
        if not exception:
            print("storing mocked", name)
            just.write(good, name)
            return good
        else:
            try:
                print("load mocked", name, "ignoring exception:")
                print(exception)
                return just.read(name)
            except:
                # do not raise "this" exception, but the original
                raise exception
    elif exception is not None:
        raise exception


def donotrun(fn, args):
    if get_env() == "dev":
        return
    return fn(args)


class Mockle():

    def __init__(self, name, fn, args=None):
        self.env = get_env()
        self.name = get_path(name)
        self.fn = fn
        self.args = args if args is not None else []

    def __enter__(self):
        try:
            good = self.fn(self.args)
        except Exception as e:
            exception = e
        if self.env == "dev" and exception:
            try:
                print("load mocked", self.name, "ignoring exception:")
                print(exception)
                return just.read(self.name)
            except:
                # do not raise this exception, but the original
                raise exception
        elif self.env == "dev" and good is not None:
            print("storing mocked", self.name)
            just.write(good, self.name)
            return good
        elif exception:
            raise exception

    def __exit__(self, *args):
        pass


# try:
#     data = just.read("wifi")
#     mockle("hihawifi", good=data)
# except Exception as e:
#     data = mockle("hihawifi", exception=e)

# with Mockle("hihawifi", just.read, "wifasdfi") as data:
#     print("data length", len(data))
