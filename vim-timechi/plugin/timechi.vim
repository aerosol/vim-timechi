if exists("g:timechi_loaded")
    finish
endif

if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

let g:timechi_loaded = 1
let s:plugin_dir = expand('<sfile>:p:h')

function! s:InitTimeChi()
python << EOF
import vim, sys
plugin_dir = vim.eval("s:plugin_dir")
sys.path.append(plugin_dir)

import timechi
timechi.get_timer()
EOF
endfunction

call s:InitTimeChi()

function! s:Event(event)
python << EOF
import vim
import timechi
event = vim.eval("a:event")
timechi.get_timer().report_event(event)
EOF
endfunction


autocmd InsertEnter * call s:Event('i_mode_entered')
autocmd InsertLeave * call s:Event('i_mode_left')

autocmd CursorHold,CursorHoldI,FocusLost * call s:Event('idle')

autocmd CursorMoved,CursorMovedI,FocusGained,VimResized,WinEnter,WinLeave,
        \CmdwinEnter,CmdwinLeave,BufNewFile,BufRead,BufWrite,BufCreate,
        \BufAdd,BufDelete,BufEnter,BufNew * call s:Event('busy')

autocmd BufWrite * call s:Event('save')
autocmd VimLeavePre * call s:Event('save')


