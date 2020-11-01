function! SelectAlbum()
  let c_line = getline(".") " OK
  if l:c_line !~# "^======== .*mp3$"
    echom "DOESN'T MATCH"
  else
    execute "normal!_dWA Album"
    execute "normal!jdj"
  endif
endfunction

function! SelectTitle()
  let l:c_line = getline(".")
  if l:c_line !~# "^======== .*mp3$"
    echom "DOESN'T MATCH"
  else
    execute "normal!_dWA Title"
    execute "normal!jdj"
  endif
endfunction

augroup podcastrename
  autocmd!
  autocmd FileType podcastrename execute "normal!ggO# Lines starting with a # will be discarded"
  autocmd FileType podcastrename execute "normal!ggO# Press a to select \"Album\", press t to select \"Title\""
  autocmd FileType podcastrename execute "normal!2Go"
  autocmd FileType podcastrename execute "normal!2Go"
  autocmd FileType podcastrename nnoremap a :call SelectAlbum()<cr>
  autocmd FileType podcastrename nnoremap t :call SelectTitle()<cr>
  autocmd FileType podcastrename syntax match Title "^======== .*\.mp3"
  autocmd FileType podcastrename syntax match GruvboxBlueSign "^.*.mp3 \(Album\|Title\)$"
  autocmd FileType podcastrename syntax match Comment "^\s*#.*$"
augroup END
