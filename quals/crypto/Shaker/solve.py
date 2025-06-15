from pwn import remote, success, warn, info
from string import ascii_letters, digits
import hashlib

# Server details
HOST = "challs.nusgreyhats.org"
PORT = 33302
io = remote(HOST, PORT)

# --- Collect samples ---
# Each call to option '2' uses one "shake" internally during reset.
# There is no limit on how many times we can call option '2' to see the output.
num_samples = 200 # Number of samples to collect (this should be enough to recover the flag)
list_of_Y_outputs = [] # To store the 64-byte outputs (as lists of ints)

info(f"Collecting {num_samples} samples...")
for _ in range(num_samples):
    # Choose "See inside" option
    io.sendlineafter(b"> ", b"2") 

    # Receive the output line "Result: aabbcc..."
    line = io.recvline().strip().decode()

    # Extract and store the byte array from the line
    hex_output = line.split("Result: ")[1]
    Y = bytes.fromhex(hex_output)
    list_of_Y_outputs.append(list(Y))

# --- Determine the XOR key x ---
CHARACTER_WHITELIST = ascii_letters + digits + "_{}"  # Whitelisted characters for the flag
recovered_x = [-1] * 64 # Initialize with -1 to indicate not found
possible_x_byte_values = list(range(256))

info("Determining the 64-byte XOR key 'x'...")
all_x_i_uniquely_determined = True
for i in range(64): # For each byte position/column of x
    # S_i contains all observed bytes at this position 'i' across all samples
    S_i = [Y[i] for Y in list_of_Y_outputs]
    
    candidate_x_values_for_i = []
    for guess_x_val in possible_x_byte_values:
        is_plausible_x_byte = True
        for y_byte_in_S_i in S_i:
            # If guess_x_val is correct, then y_byte_in_S_i ^ guess_x_val should be a flag character
            decrypted_char_code = y_byte_in_S_i ^ guess_x_val
            if chr(decrypted_char_code) not in CHARACTER_WHITELIST:
                is_plausible_x_byte = False
                break
        if is_plausible_x_byte:
            candidate_x_values_for_i.append(guess_x_val)
    
    if len(candidate_x_values_for_i) == 1:
        # Unique candidate found for x[i]
        recovered_x[i] = candidate_x_values_for_i[0]
    else:
        warn(f"Byte x[{i}] has {len(candidate_x_values_for_i)} candidates: {candidate_x_values_for_i}.")
        all_x_i_uniquely_determined = False
        if candidate_x_values_for_i: # If there are multiple candidates, pick the first one (a guess)
            recovered_x[i] = candidate_x_values_for_i[0]
            warn(f"  Using the first candidate for x[{i}]: {recovered_x[i]}")
        else: # No candidates found
            warn(f"  No valid candidate found for x[{i}]. This is problematic.")
            # recovered_x[i] remains -1

if not all_x_i_uniquely_determined:
    warn("Some bytes of 'x' were not uniquely determined. The derived flag might be incorrect.")
if any(val == -1 for val in recovered_x):
    warn("Failed to determine all bytes of 'x'. Cannot proceed to flag recovery.")
    io.close()
    exit(1)

info(f"Recovered x: {bytes(recovered_x).hex()}...")

# --- Calculate the candidate flag ---
# Y_0 is the first output collected: list_of_Y_outputs[0]
# Y_0 = Flag ^ x  =>  Flag = Y_0 ^ x
Y_0 = list_of_Y_outputs[0] 
candidate_flag_bytes_list = [Y_0[i] ^ recovered_x[i] for i in range(64)]
candidate_flag_bytes = bytes(candidate_flag_bytes_list)

# --- Verify the flag ---
target_md5 = "4839d730994228d53f64f0dca6488f8d"
info(f"Target MD5: {target_md5}")

md5_hash_of_candidate = hashlib.md5(candidate_flag_bytes).hexdigest()
info(f"MD5 of candidate flag: {md5_hash_of_candidate}")

candidate_flag_str = candidate_flag_bytes.decode('ascii')
info(f"Candidate flag string: {candidate_flag_str}")

if md5_hash_of_candidate == target_md5:
    success(f"🎉 Flag successfully recovered: {candidate_flag_str}")
else:
    warn("Flag verification failed. MD5 hash does not match.")
    warn("This could be due to non-unique x_i determination or incorrect character range assumption.")

# --- Exit gracefully ---
# Choose "Exit" option
io.sendlineafter(b"> ", b"3")
io.close()