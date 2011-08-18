" TimeChi
" https://github.com/aerosol/vim-timechi
"
if exists("g:timechi_loaded")
    finish
endif

if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

if !exists("g:timechi_debug")
    let g:timechi_debug = 0
endif

let s:plugin_dir = expand('<sfile>:p:h')

function! s:InitTimeChi()
python << EOF
import vim, sys
plugin_dir = vim.eval("s:plugin_dir")
sys.path.append(plugin_dir)
import timechi
timechi.session()
EOF
endfunction

function! s:Event(event)
python << EOF
import vim
import timechi
event = vim.eval("a:event")
timechi.session().report_event(event)
EOF
endfunction

if !exists("g:timechi_loaded")
    call s:InitTimeChi()
    autocmd InsertEnter * call s:Event('i_mode_entered')
    autocmd InsertLeave * call s:Event('i_mode_left')

    autocmd CursorHold,CursorHoldI,FocusLost * call s:Event('idle')

    autocmd CursorMoved,CursorMovedI,FocusGained,VimResized,WinEnter,WinLeave,
            \CmdwinEnter,CmdwinLeave,BufNewFile,BufRead,BufWrite,BufCreate,
            \BufAdd,BufDelete,BufEnter,BufNew * call s:Event('ping')

    autocmd BufWrite * call s:Event('save')
    " VimLeave isn't that obvious, it's triggered also when quitting *a buffer*
    " autocmd VimLeave * call s:Event('quit')
    let g:timechi_loaded = 1
endif

