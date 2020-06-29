# Breton Mutation Starter Project

## Challenges

- Some mutation triggers are ambiguous, with some homographs/homophones
  triggering different mutations. This implementation ignores these ambiguous
  triggers. A result of this is that this implementation does not apply the
  Breton mixed mutation at all, since its triggers are all homographs/homophones
  with words that trigger a different mutation.
- For the soft mutation, some initial consonants are ambiguous about whether the
  mutation has applied or not without additional context / knowledge of the
  language. For example initial b could have been an underlying p that mutated
  to b, or a b that failed to mutate to v. this implementation ignores words
  after a soft mutation trigger that start with b, d, and g.
