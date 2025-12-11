from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
import html
from sqlalchemy.orm import sessionmaker
from connection import engine, VerbForm

from translations import geo


# Your database query function (example)
def group_by_screeve(result):
    screeves = {}
    for item in result:
        if item.screeve not in screeves:
            screeves[item.screeve] = [item]
        else:
            screeves[item.screeve].append(item)
    return screeves


def rearrange(result):
    rearranged = {}
    for screeve in result:
        forms = result[screeve]
        matrix = [['' for _ in range(7)] for _ in range(7)]
        for row in range(6):
            matrix[0][row+1] = f'S:{row%3+1}{"sg" if row < 3 else "pl"}'
        for col in range(6):
            matrix[col+1][0] = f'O:{col%3+1}{"sg" if col < 3 else "pl"}'
        for form in forms:
            if form.subject_number == 'sg':
                x = form.subject_person
            elif form.subject_number == 'pl':
                x = 3 + form.subject_person
            else:
                raise ValueError(f'Invalid subject {form.subject_number}')
            if form.object_number == 'sg':
                y = form.object_person
            elif form.object_number == 'pl':
                y = 3 + form.object_person
            else:
                raise ValueError(f'Invalid object {form.object_number}')

            matrix[y][x] = form.word_form
        rearranged[screeve] = matrix
    return rearranged


def get_data_from_db(param):
    session = sessionmaker(bind=engine)()
    result = session.query(VerbForm).filter_by(word_form=param).all()
    if len(result) > 0 and not result[0].screeve.endswith('_prfv'):
        result = session.query(VerbForm).filter_by(word_form=param, preverb=result[0].preverb).all()
    unique_verbs = {r.verb for r in result}
    paradigms = {}
    for verb in unique_verbs:
        paradigm = session.query(VerbForm).filter_by(verb=verb, preverb=result[0].preverb).all()
        paradigm = group_by_screeve(paradigm)
        paradigm = rearrange(paradigm)
        paradigms[verb] = paradigm
    session.close()
    return result, paradigms


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Root page with form
        if path == '/' or path == '':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>ზმნის ფორმის ძიება</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        max-width: 600px;
                        margin: 50px auto;
                        padding: 20px;
                    }
                    input[type="text"] {
                        width: 300px;
                        padding: 8px;
                        font-size: 16px;
                    }
                    button {
                        padding: 8px 20px;
                        font-size: 16px;
                        cursor: pointer;
                    }
                </style>
            </head>
            <body>
                <h1>ზმნის ფორმის ძიება</h1>
                <form action="/results" method="get">
                    <input type="text" name="query" placeholder="ჩაწერე ნებისმიერი ზმნის ფორმა" required>
                    <button type="submit">ძიება</button>
                </form>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode())

        # Results page
        elif path == '/results':
            query_params = parse_qs(parsed_path.query)
            query_value = html.unescape(query_params.get('query', [''])[0])
            # Escape HTML to prevent XSS
            safe_query = html.escape(query_value)

            # Get data from database
            result, paradigms = get_data_from_db(query_value)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            verb_form_dicts = ""
            for row in result:
                row_dict = dict((col, getattr(row, col)) for col in row.__table__.columns.keys())
                verb_form_dicts += f"\t\t<table>"
                verb_form_dicts += f"\t\t\t<tr>"
                for key in row_dict:
                    if key != 'id':
                        verb_form_dicts += f"\t\t\t\t<th>{geo.get(key, key)}</th>"
                verb_form_dicts += f"\t\t\t</tr>"
                verb_form_dicts += f"\t\t\t<tr>"
                for key in row_dict:
                    if key != 'id':
                        value = row_dict[key]
                        verb_form_dicts += f"\t\t\t\t<td>{geo.get(value, value)}</td>"
                verb_form_dicts += f"\t\t\t</tr>"
                verb_form_dicts += f"\t\t</table>"

            html_tables = ""
            for verb in paradigms:
                paradigm = paradigms[verb]
                html_tables += f"\t\t<h3>{verb}</h3>\n"
                for screeve in paradigm:
                    html_tables += f"\t\t<h4>{geo[screeve]}</h4>\n"
                    html_tables += f"\t\t<table>\n"
                    matrix = paradigm[screeve]
                    for row in matrix:
                        html_tables += f"\t\t\t<tr>\n"
                        for form in row:
                            html_tables += f"\t\t\t\t<td>{form}</td>\n"
                        html_tables += f"\t\t\t</tr>\n"
                    html_tables += f"\t\t</table>\n"

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>ზმნის ძიების შედეგები</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        max-width: 800px;
                        margin: 50px auto;
                        padding: 20px;
                    }}
                    .back-link {{
                        display: inline-block;
                        margin-bottom: 20px;
                        color: #0066cc;
                        text-decoration: none;
                    }}
                    .back-link:hover {{
                        text-decoration: underline;
                    }}
                    table {{
                        border: 1px solid black;
                        border-collapse: collapse;
                        width: 100%;
                    }}
                    th, td {{
                        border: 1px solid black;
                        padding: 5px;
                    }}
                </style>
            </head>
            <body>
                <a href="/" class="back-link">← უკან ძიებასთან</a>
                <h1>საძიებო ფორმა: {safe_query}</h1>
                <div>
                    {verb_form_dicts}
                </div>
                <div>
                    {html_tables}
                </div>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode())

        else:
            # 404 for other paths
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>404 - Page Not Found</h1>")

    def log_message(self, format, *args):
        # Optional: customize logging or suppress it
        print(f"{self.address_string()} - {format % args}")


def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f"Server running on http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.shutdown()


if __name__ == '__main__':
    run_server()