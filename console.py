#!/usr/bin/python3
'''
    Implementing the console for the HBnB project.
'''
import cmd
import shlex
import models
from ast import literal_eval
from models import storage


class HBNBCommand(cmd.Cmd):
    """Entry point of the command interpreter."""
    prompt = ("(hbnb) ")

    def do_quit(self, _):
        """Command to exit the program."""
        return True

    def do_EOF(self, _):
        """Exits after receiving the End of File"""
        return True

    def do_create(self, args):
        """
        Create a new instance of class BaseModel
        and save it to the JSON file.
       """
        if len(args) == 0:
            print("** class name missing **")
            return
        try:
            args = shlex.split(args)
            new_instance = literal_eval(args[0])()
            for i in args[1:]:
                try:
                    key = i.split("=")[0]
                    value = i.split("=")[1]
                    if hasattr(new_instance, key) is True:
                        value = value.replace("_", " ")
                        try:
                            value = literal_eval(value)
                        except (ValueError, IndexError):
                            pass
                        setattr(new_instance, key, value)
                except (ValueError, IndexError):
                    pass
            new_instance.save()
            print(new_instance.id)
        except (ValueError, IndexError):
            print("** class doesn't exist **")
            return

    def do_show(self, args):
        """
        Print the string representation of an instance
        based on the class name and id given as args.
        """
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        obj_dict = storage.all(args[0])
        try:
            literal_eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        key = args[0] + "." + args[1]
        try:
            value = obj_dict[key]
            print(value)
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id."""
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return

        class_name = args[0]
        class_id = args[1]
        storage.reload()
        obj_dict = storage.all()

        try:
            literal_eval(class_name)
        except NameError:
            print("** class doesn't exist **")
            return

        key = class_name + "." + class_id

        try:
            del obj_dict[key]
        except KeyError:
            print("** no instance found **")
        storage.save()

    def do_all(self, args):
        """
        Prints all string representation of all instances
        based or not on the class name.
        """
        args = args.split(" ")
        obj_list = []
        objects = storage.all(args[0])
        try:
            if args[0] != "":
                models.classes[args[0]]
        except (KeyError, NameError):
            print("** class doesn't exist **")
            return
        try:
            for _, val in objects.items():
                obj_list.append(val)
        except (ValueError, IndexError):
            pass
        print(obj_list)

    def do_update(self, args):
        """
        Update an instance based on the
        class name and id sent as args.
        """
        storage.reload()
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return

        try:
            literal_eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        key = args[0] + "." + args[1]
        obj_dict = storage.all()
        try:
            obj_value = obj_dict[key]
        except KeyError:
            print("** no instance found **")
            return
        try:
            attr_type = type(getattr(obj_value, args[2]))
            args[3] = attr_type(args[3])
        except AttributeError:
            pass
        setattr(obj_value, args[2], args[3])
        obj_value.save()

    def emptyline(self):
        """
            Prevents printing anything when an empty line is passed.
        """
        pass

    def do_count(self, args):
        """
            Counts/retrieves the number of instances.
        """
        obj_list = []
        storage.reload()
        objects = storage.all()
        try:
            if len(args) != 0:
                eval(args)
        except NameError:
            print("** class doesn't exist **")
            return
        for key, val in objects.items():
            if len(args) != 0:
                if type(val) is eval(args):
                    obj_list.append(val)
            else:
                obj_list.append(val)
        print(len(obj_list))

    def default(self, args):
        """
            Catches all the function names that are not expicitly defined.
        """
        functions = {"all": self.do_all, "update": self.do_update,
                     "show": self.do_show, "count": self.do_count,
                     "destroy": self.do_destroy, "update": self.do_update}
        args = (args.replace("(", ".").replace(")", ".")
                .replace('"', "").replace(",", "").split("."))

        try:
            cmd_arg = args[0] + " " + args[2]
            func = functions[args[1]]
            func(cmd_arg)
        except (ValueError, IndexError):
            print("*** Unknown syntax:", args[0])


if __name__ == "__main__":
    '''
        Entry point for the loop.
    '''
    HBNBCommand().cmdloop()
