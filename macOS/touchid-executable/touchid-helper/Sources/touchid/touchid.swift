// The Swift Programming Language
// https://docs.swift.org/swift-book

import Foundation
import LocalAuthentication

let reason = CommandLine.arguments.dropFirst().joined(separator: " ")

if reason.isEmpty {
    fputs("Usage: touchid <reason>\n", stderr)
    exit(2)
}

let context = LAContext()

context.localizedCancelTitle = "Cancel"

var authError: NSError?

guard context.canEvaluatePolicy(
    .deviceOwnerAuthenticationWithBiometrics,
    error: &authError
) else {
    if let error = authError {
        fputs("Touch ID unavailable: \(error.localizedDescription)\n", stderr)
    } else {
        fputs("Touch ID unavailable\n", stderr)
    }

    exit(2)
}

let semaphore = DispatchSemaphore(value: 0)
var authenticated = false

context.evaluatePolicy(
    .deviceOwnerAuthenticationWithBiometrics,
    localizedReason: reason
) { success, error in

    authenticated = success

    if let error = error {
        fputs("\(error.localizedDescription)\n", stderr)
    }

    semaphore.signal()
}

semaphore.wait()

exit(authenticated ? 0 : 1)
