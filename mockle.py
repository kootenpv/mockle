import os
import just


def get_env():
    return os.environ.get("PYTHON_ENV", "dev")


def mockle(name, good=None, exception=""):
    name = name + ".pkl"
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

    def __init__(self, name, fn, args):
        self.env = get_env()
        self.name = name + ".pkl"
        self.fn = fn
        self.args = args

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
