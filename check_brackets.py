import sys
import os

def check_brackets():
    sys.stdout.reconfigure(encoding='utf-8')
    f2 = 'src_extracted/dist/assets/index-CealnApy.js'
    f1 = 'resources/app_original/dist/assets/index-CealnApy.js'
    
    if not os.path.exists(f2) or not os.path.exists(f1):
        print("Required files not found")
        return
        
    with open(f1, 'r', encoding='utf-8') as f:
        c1 = f.read()
    with open(f2, 'r', encoding='utf-8') as f:
        code = f.read()

    # Find first diff index
    i = 0
    while i < len(c1) and i < len(code) and c1[i] == code[i]:
        i += 1

    j2 = len(code) - 1
    j1 = len(c1) - 1
    while j1 >= i and j2 >= i and c1[j1] == code[j2]:
        j1 -= 1
        j2 -= 1

    stack = []
    state_stack = ['NORMAL']
    pairs = {')': '(', ']': '[', '}': '{'}
    
    # Parse from 0 to i to get initial stack
    idx = 0
    while idx < i:
        state = state_stack[-1]
        if state in ['NORMAL', 'TEMPLATE_EXPR']:
            if idx + 1 < i and code[idx] == '/' and code[idx+1] == '/':
                idx += 2
                while idx < i and code[idx] != '\n':
                    idx += 1
                continue
            if idx + 1 < i and code[idx] == '/' and code[idx+1] == '*':
                idx += 2
                while idx + 1 < i and not (code[idx] == '*' and code[idx+1] == '/'):
                    idx += 1
                idx += 2
                continue
        if state in ['NORMAL', 'TEMPLATE_EXPR']:
            if code[idx] in ['\'', '\"']:
                quote = code[idx]
                idx += 1
                while idx < i and code[idx] != quote:
                    if code[idx] == '\\':
                        idx += 2
                    else:
                        idx += 1
                idx += 1
                continue
        if state in ['NORMAL', 'TEMPLATE_EXPR']:
            if code[idx] == '`':
                state_stack.append('TEMPLATE_LITERAL')
                idx += 1
                continue
        elif state == 'TEMPLATE_LITERAL':
            if code[idx] == '`':
                state_stack.pop()
                idx += 1
                continue
            elif code[idx] == '\\':
                idx += 2
                continue
            elif idx + 1 < i and code[idx] == '$' and code[idx+1] == '{':
                state_stack.append('TEMPLATE_EXPR')
                stack.append(('${', idx))
                idx += 2
                continue
        if state in ['NORMAL', 'TEMPLATE_EXPR']:
            if code[idx] == '/':
                prev_idx = idx - 1
                while prev_idx >= 0 and code[prev_idx].isspace():
                    prev_idx -= 1
                if prev_idx >= 0 and not (code[prev_idx].isalnum() or code[prev_idx] in ['_', ')', ']', '}']):
                    idx += 1
                    while idx < i and code[idx] != '/':
                        if code[idx] == '\\':
                            idx += 2
                        else:
                            idx += 1
                    idx += 1
                    continue
        char = code[idx]
        if char in '([{':
            stack.append((char, idx))
        elif char in ')]}':
            if stack:
                top_char, top_pos = stack.pop()
                if char == '}':
                    if top_char == '${' and state_stack[-1] == 'TEMPLATE_EXPR':
                        state_stack.pop()
        idx += 1

    print('Initial stack size at diff start:', len(stack))
    print('Initial stack:', [x[0] for x in stack])

    diff_start = i
    diff_end = j2 + 1
    print('Parsing diff block from', diff_start, 'to', diff_end)

    idx = diff_start
    while idx < diff_end:
        state = state_stack[-1]
        if state in ['NORMAL', 'TEMPLATE_EXPR']:
            if idx + 1 < diff_end and code[idx] == '/' and code[idx+1] == '/':
                idx += 2
                while idx < diff_end and code[idx] != '\n':
                    idx += 1
                continue
            if idx + 1 < diff_end and code[idx] == '/' and code[idx+1] == '*':
                idx += 2
                while idx + 1 < diff_end and not (code[idx] == '*' and code[idx+1] == '/'):
                    idx += 1
                idx += 2
                continue
        if state in ['NORMAL', 'TEMPLATE_EXPR']:
            if code[idx] in ['\'', '\"']:
                quote = code[idx]
                idx += 1
                while idx < diff_end and code[idx] != quote:
                    if code[idx] == '\\':
                        idx += 2
                    else:
                        idx += 1
                idx += 1
                continue
        if state in ['NORMAL', 'TEMPLATE_EXPR']:
            if code[idx] == '`':
                state_stack.append('TEMPLATE_LITERAL')
                idx += 1
                continue
        elif state == 'TEMPLATE_LITERAL':
            if code[idx] == '`':
                state_stack.pop()
                idx += 1
                continue
            elif code[idx] == '\\':
                idx += 2
                continue
            elif idx + 1 < diff_end and code[idx] == '$' and code[idx+1] == '{':
                state_stack.append('TEMPLATE_EXPR')
                stack.append(('${', idx))
                idx += 2
                continue
        if state in ['NORMAL', 'TEMPLATE_EXPR']:
            if code[idx] == '/':
                prev_idx = idx - 1
                while prev_idx >= 0 and code[prev_idx].isspace():
                    prev_idx -= 1
                if prev_idx >= 0 and not (code[prev_idx].isalnum() or code[prev_idx] in ['_', ')', ']', '}']):
                    idx += 1
                    while idx < diff_end and code[idx] != '/':
                        if code[idx] == '\\':
                            idx += 2
                        else:
                            idx += 1
                    idx += 1
                    continue
        char = code[idx]
        if char in '([{':
            stack.append((char, idx))
        elif char in ')]}':
            if not stack:
                print(f"Unmatched closing char {char} at pos {idx}: {repr(code[max(0, idx-40):idx+40])}")
                break
            else:
                top_char, top_pos = stack.pop()
                if char == '}':
                    if top_char == '${':
                        if state_stack[-1] == 'TEMPLATE_EXPR':
                            state_stack.pop()
                        else:
                            print('State mismatch')
                            break
                    elif top_char != '{':
                        print(f"Mismatch: opened {top_char} at {top_pos} but closed {char} at {idx}")
                        print("Opening context:", repr(code[max(0, top_pos-40):top_pos+40]))
                        print("Closing context:", repr(code[max(0, idx-40):idx+40]))
                        break
                else:
                    if top_char != pairs[char]:
                        print(f"Mismatch: opened {top_char} at {top_pos} but closed {char} at {idx}")
                        print("Opening context:", repr(code[max(0, top_pos-40):top_pos+40]))
                        print("Closing context:", repr(code[max(0, idx-40):idx+40]))
                        break
        idx += 1

    print('Done parsing diff block!')

if __name__ == '__main__':
    check_brackets()
