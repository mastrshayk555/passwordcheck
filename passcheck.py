# Change this so that it runs from a platform that will not save the input
# Text file is one option

# import necessary packages
import requests  # pulls from websites
import hashlib  # Allows us review and alter the hash(encrypted password) string
import sys  # idk yet


# Creating function to access password checking webpage
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char  # turn url + characters(password) we're looking to check
    res = requests.get(url)  # utilizing the requests lib to access the url
    if res.status_code != 200:  # checking and notifying should requests status code not return 200
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again.')
    return res


# Note: 100 == Informational, 200 == Success, 300 == Redirect, 400 == Client Error, 500 == Server Error

# requests_api_data()


# Function to report how many times this password has been found
def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in
              hashes.text.splitlines())  # this splits the hash code from the number of times found with th ':' and
    # assigns it to hashes
    for h, count in hashes:  # h == the entire hash. count == number of times found (after the ':')
        if h == hash_to_check:  # if the hashes are == then tell me how many times they appeared
            return count
    return 0  # otherwise move along with zero found


# Checks to see if the password exists in API response
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode(
        'utf-8')).hexdigest().upper()  # calls hashlib module with a SHA1 hash format that in turn encodes the string
    # in hexdigest(hex decimal only) and makes all chars uppercase.
    first5_char, tail = sha1password[:5], sha1password[
                                          5:]  # Splits the first 5 characters rom the whole hash for easier referencing
    response = request_api_data(first5_char)  # Calls function to run (or query) 5 char hash thru site checker
    # print(first5_char, tail) #Uncomment this if you want to see the hash reported
    return get_password_leaks_count(response, tail)  # Calls function to run hash through and report


# Running the password entered in terminal
def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times... You should probably change your password.')
        else:
            print(f"{password} was NOT found. OK to proceed.")
    return 'done!'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
