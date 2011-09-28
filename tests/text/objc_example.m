#import "afile.h"

NSDictionary *dictionary = [NSDictionary dictionaryWithObjectsAndKeys:
                                @"quattuor", @"four", @"quinque", @"five", nil];

for (NSString *key in dictionary) {
    NSLog(@"English: %@, Latin: %@", key, [dictionary valueForKey:key]);
}

