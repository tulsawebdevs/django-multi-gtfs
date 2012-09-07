from csv import writer
from datetime import time, date
from StringIO import StringIO


def parse_time(time_string):
    """Parse a GTFS-formatted time into a time and day

    Keyword Arguments:
    time_string -- A 'HH:MM:SS' formatted time

    Return is a tuple:
    time -- a datetime.time
    day -- 0 if the entered time was under 24 hours, 1 if over

    If time_string is falsy, (None, None) is returned
    """
    if time_string:
        hour, minute, second = [int(p) for p in time_string.split(':')]
        day = 0
        while hour > 23:
            hour -= 24
            day += 1
        return time(hour, minute, second), day
    return None, None


def create_csv(queryset, csv_names):
    """Turn a queryset into a CSV export

    Keyword Arguments:
    queryset -- A queryset with at least one record
    csv_names -- A sequnce of (csv column, field name) pairs

    A field name can follow relations, such as 'field1__subfield2'
    """
    columns, fields = zip(*csv_names)
    rows = [columns]
    for item in queryset.order_by(*fields):
        row = []
        for csv_name, field_name in csv_names:
            obj = item
            while obj and '__' in field_name:
                parent_field, field_name = field_name.split('__', 1)
                obj = getattr(obj, parent_field)
            field = getattr(obj, field_name) if obj else ''
            if isinstance(field, date):
                row.append(field.strftime('%Y%m%d'))
            elif isinstance(field, bool):
                row.append(1 if field else 0)
            elif field is None:
                row.append('')
            else:
                row.append(str(field))
        rows.append(row)
    out = StringIO()
    writer(out, lineterminator='\n').writerows(rows)
    return out.getvalue()
