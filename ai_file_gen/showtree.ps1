function print-directory([string]$path, [int]$indent, [int]$depth) {
    if ($depth -le 0) { return }
    $files = Get-ChildItem -Path $path

    foreach ($file in $files) {
        "`t" * $indent + $file.Name
        if ($file.PSIsContainer) { print-directory $file.FullName ($indent+1) ($depth-1) }
    }
}
print-directory (pwd) 0 2