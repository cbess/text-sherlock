#import "afile.h"

NSDictionary *dictionary = [NSDictionary dictionaryWithObjectsAndKeys:
                                @"quattuor", @"four", @"quinque", @"five", nil];

for (NSString *key in dictionary) {
    NSString *value = [dictionary valueForKey:key];
    NSLog(@"English: %@, Latin: %@", key, value);
}

