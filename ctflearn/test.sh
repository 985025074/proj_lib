    #!/bin/sh

    # Python will hit it's recursion limit
    # If you supply just 4 less than the recursion limit
    # I assume this means there's a few objects on the call stack first
    # Probably: __main__, print, json.loads, and input.

    n="$(python3 -c 'import math; import sys; sys.stdout.write(str(math.floor(sys.getrecursionlimit() - 4)))')"

    echo "N: $n"

    # Obviously invalid, but unparseable without matching pair
    # JSON's grammar is... Not good at being partially parsed.
    left="$(yes [ | head -n "$n" | tr -d '\n')"

    # Rather than exploding with the expected decodeError
    # This will explode with a RecursionError
    # Which naturally thrashes the memory cache.
    echo "$left" | python3 -c 'import json; print(json.loads(input()))'