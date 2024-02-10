from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
@app.route('/<file_name>')
def display_file(file_name=None):
    try:
        if file_name is None:
            file_name = 'file1.txt'
            
        start_line = request.args.get('start_line')
        end_line = request.args.get('end_line')

        
        if start_line is not None:
            start_line = int(start_line)
        if end_line is not None:
            end_line = int(end_line)

        with open(file_name, 'rb') as file:
            
            raw_data = file.read(4)
            file_encoding = 'utf-8'  

            
            if raw_data.startswith(b'\xff\xfe') or raw_data.startswith(b'\xfe\xff'):
                file_encoding = 'utf-16'  
            elif raw_data.startswith(b'\xef\xbb\xbf'):
                file_encoding = 'utf-8-sig'  

            
            file.seek(0)
            content = file.read().decode(file_encoding)

        
        lines = content.splitlines()[start_line:end_line]

        
        content = '\n'.join(lines)
        return render_template('file_display.html', content=content)

    except Exception as e:
        return render_template('error.html', error=str(e))


if __name__ == '__main__':
    app.run(debug=True)
