-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Known:
--  * Theft took place on July 28
--  * Theft took place on Humphrey Street

-- Goal:
--  * Identify the thief
--  * Identify where the thief escaped to
--  * Identify who the thief's accomplice was who helped them escape town

-- Suspects:
--  * Vanessa
--  * Barry
--  * Iman x2
--  * Sofia x2
--  * Luca x2
--  * Diana x3
--  * Kelsey x2
--  * Bruce x3
--  * Brooke
--  * Kenny x2
--  * Taylor x2
--  * Benista x2
--  * Carina

-- Get structure of database
.schema

-- Find crime scene description
SELECT description FROM crime_scene_reports
WHERE month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Description:
-- Theft of the CS50 duck took place at 10:15 AM at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present
-- at the time - each of their interview transcripts mentions the bakery.
-- Littering took place at 16:36. No known witnesses.

-- Find the three interviews mentioned in the crime scene description.
SELECT * FROM interviews
WHERE transcript LIKE '%bakery%'
      AND month = 7 AND day = 28;

-- Witnesses    Transcript
-- Ruth         Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security
--              footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
-- Eugene       I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking
--              by the ATM on Leggett Street and saw the thief there withdrawing some money.
-- Raymond      As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say
--              that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the
--              phone to purchase the flight ticket.

-- Access bakery security logs for the day of the crime
SELECT id, hour, minute, activity, license_plate FROM bakery_security_logs
WHERE month = 7 AND day = 28
AND hour < 11;

-- Identify people exiting the bakery within ten minutes of the theft
SELECT name FROM people
WHERE license_plate IN (
    SELECT license_plate FROM bakery_security_logs
    WHERE month = 7 AND day = 28
    AND hour = 10 AND minute BETWEEN 15 AND 25
);

-- Suspects: Vanessa, Barry, Iman, Sofia, Luca, Diana, Kelsey, Bruce

-- Access ATM logs for the day of the crime at Leggett Street
SELECT * FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street';

-- Identify people making ATM withdrawals at this time
SELECT name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE bank_accounts.account_number IN (
    SELECT account_number FROM atm_transactions
    WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street'
)
AND month = 7 AND day = 28 AND transaction_type = 'withdraw';

-- Suspects: Bruce, Diana, Brooke, Kenny, Iman, Luca, Taylor, Benista

-- Access phone call logs for the day of the crime with a duration of less than a minute
SELECT * FROM phone_calls
WHERE month = 7 AND day = 28 AND duration < 60;

-- Identify people making phone calls at this time
SELECT name FROM people
WHERE phone_number IN (
    SELECT caller FROM phone_calls
    WHERE month = 7 AND day = 28 AND duration < 60
);

-- Suspects: Kenny, Sofia, Benista, Taylor, Diana, Kelsey, Bruce, Carina

-- Two prime suspects: Diana and Bruce

-- Identify phone call receiver for their respecive calls
SELECT name FROM people
WHERE phone_number IN (
    SELECT receiver FROM people
    JOIN phone_calls on people.phone_number = phone_calls.caller
    WHERE (name = 'Diana' OR name = 'Bruce')
    AND month = 7 AND day = 28 AND duration < 60
);

-- Diana -> Philip
-- Bruce -> Robin

-- Identify the destination of the earliest flight out of Fiftyville July 29
SELECT * FROM airports
WHERE id IN (
    SELECT destination_airport_id FROM flights
    WHERE month = 7 AND day = 29
    ORDER BY hour
    LIMIT 1
);

-- Destination: LaGuardia Airport, New York

-- Identify prime suspect on the flight
SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
WHERE flights.id = (
    SELECT id FROM flights
    WHERE month = 7 AND day = 29
    ORDER BY hour
    LIMIT 1
);

-- Bruce was on the flight. Hence, all evidence suggest that he is the thief.