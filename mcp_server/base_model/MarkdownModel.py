from pydantic import BaseModel
from typing import get_args, get_origin, Union, Literal, Optional, Dict, List

class GetIdModel(BaseModel):
    id: Optional[int] = None 
    
    def get_id(self):
        return self.id

class MarkdownModel(BaseModel):
    def str(self, indent: int = 0, verbose: bool = False) -> str:
        lines = []
        prefix = "  " * indent
        fields = self.model_fields if hasattr(self, 'model_fields') else self.__fields__

        # docstring модели
        if verbose and self.__doc__:
            lines.append(f"{prefix}{self.__doc__.strip()}")

        for key, field in fields.items():
            value = getattr(self, key, None)
            if value in [None, "", {}, []]:
                continue

            description = field.description if hasattr(field, 'description') else None
            field_label = f"**{key}**"
            if verbose and description:
                field_label += f" _({description})_"

            # вложенная модель
            if isinstance(value, MarkdownModel):
                lines.append(f"{prefix}{field_label}:\n{value.str(indent + 1, verbose)}")

            # список
            elif isinstance(value, list):
                lines.append(f"{prefix}{field_label}:")
                for item in value:
                    if isinstance(item, MarkdownModel):
                        item_lines = item.str(indent + 2, verbose).splitlines()
                        if item_lines:
                            # первый элемент с "-", остальные без
                            lines.append(f"{'  ' * (indent + 1)}- {item_lines[0].lstrip()}")
                            lines.extend(f"{'  ' * (indent + 1)}  {line.lstrip()}" for line in item_lines[1:])
                    else:
                        lines.append(f"{'  ' * (indent + 1)}- {item}")

            # словарь
            elif isinstance(value, dict):
                lines.append(f"{prefix}{field_label}:")
                for k, v in value.items():
                    lines.append(f"{'  ' * (indent + 1)}- {k}: {v}")

            # обычное поле
            else:
                lines.append(f"{prefix}{field_label}: {value}")

        return "\n".join(lines)

    def __str__(self):
        return self.str(verbose=True)
    
    def json(self, verbose: bool = False) -> dict:
        result = {}
        fields = self.model_fields if hasattr(self, 'model_fields') else self.__fields__

        # Add docstring if verbose mode is on
        if verbose and self.__doc__:
            result["__doc__"] = self.__doc__.strip()

        for key, field in fields.items():
            value = getattr(self, key, None)
            if value in [None, "", {}, []]:
                continue

            # Handle nested model
            if isinstance(value, MarkdownModel):
                result[key] = value.json(verbose)

            # Handle list
            elif isinstance(value, list):
                result[key] = [
                    item.json(verbose) if isinstance(item, MarkdownModel) else item
                    for item in value
                ]

            # Handle dictionary
            elif isinstance(value, dict):
                result[key] = value

            # Handle regular field
            else:
                result[key] = value

            # Add field description if verbose mode is on
            if verbose:
                description = field.description if hasattr(field, 'description') else None
                if description:
                    if not isinstance(result[key], dict):
                        result[key] = {"value": result[key]}
                    result[key]["description"] = description

        return result
    
    @classmethod
    def schema_str(cls, indent: int = 0, verbose: bool = True) -> str:
        lines = []
        prefix = "  " * indent

        if verbose and cls.__doc__:
            lines.append(f"{prefix}{cls.__doc__.strip()}")

        fields = cls.model_fields if hasattr(cls, 'model_fields') else cls.__fields__

        def type_to_str(tp):
            origin = get_origin(tp)
            args = get_args(tp)

            # убираем Optional
            if origin is Union:
                non_none_args = [arg for arg in args if arg is not type(None)]
                return type_to_str(non_none_args[0]) if len(non_none_args) == 1 else f"Union[{', '.join(type_to_str(a) for a in non_none_args)}]"

            elif origin in (list, List):
                return f"List[{type_to_str(args[0])}]" if args else "List"

            elif origin in (dict, Dict):
                return f"Dict[{type_to_str(args[0])}, {type_to_str(args[1])}]" if len(args) == 2 else "Dict"

            elif origin is Literal:
                return f"Literal[{', '.join(repr(arg) for arg in args)}]"

            elif isinstance(tp, type):
                return tp.__name__

            return tp.__name__ if hasattr(tp, '__name__') else str(tp)

        def find_markdown_model(tp):
            """
            Рекурсивно ищет первый тип, который наследует MarkdownModel.
            """
            origin = get_origin(tp)
            args = get_args(tp)
            if origin is Union:
                for arg in args:
                    res = find_markdown_model(arg)
                    if res:
                        return res
            elif origin in (list, List, Optional):
                if args:
                    return find_markdown_model(args[0])
            elif isinstance(tp, type) and issubclass(tp, MarkdownModel):
                return tp
            return None

        for key, field in fields.items():
            description = field.description if hasattr(field, 'description') else None
            field_label = f"**{key}**"
            if verbose and description:
                field_label += f" _({description})_"

            field_type = field.annotation if hasattr(field, 'annotation') else field.outer_type_
            type_repr = type_to_str(field_type)

            # ищем вложенную MarkdownModel
            inner_type = find_markdown_model(field_type)

            if inner_type and inner_type != cls:
                lines.append(f"{prefix}{field_label}: {type_repr}")
                lines.append(inner_type.schema_str(indent + 1, verbose))
            else:
                lines.append(f"{prefix}{field_label}: {type_repr}")

        return "\n".join(lines)

    def get_class(self):
        """
        Возвращает класс экземпляра (аналог my_obj.__class__).
        """
        return self.__class__